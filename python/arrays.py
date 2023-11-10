from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, SupportsIndex


class SizeException(TypeError):
    def __init__(self, *args, **kwargs):
        super(SizeException, self).__init__(args, kwargs)


class EDogBreed(Enum):
    DOBERMAN = "doberman"
    DASCHUND = "daschund"
    BEAGLE = "beagle"


# how would I create a ArrayBuffer[Dog] for a hypothetical dog adoption app?
@dataclass
class Dog:
    name: str
    breed: EDogBreed
    date_released: datetime
    date_adopted: datetime


@dataclass
class ArrayBuffer(SupportsIndex):
    _array: bytearray

    def __init__(self, size: int):
        self._size = size
        self._array = bytearray()
        for _ in range(self._size):
            self._array.append(0)

    @property
    def size(self) -> int:
        return self._size

    def __index__(self):
        return 1

    def __getitem__(self, index: int | slice) -> Optional[List[int] | int]:
        if isinstance(index, slice):
            return [self._array[i] for i in range(*index.indices(len(self._array)))]
        elif isinstance(index, int):
            if index > self._size - 1:
                return None
            return self._array[index]

    # switch to using append?
    def __setitem__(self, index: int, value: int, offset: int = 0):
        if index < 0:
            raise IndexError("ArrayBuffer cannot index negative values")
        if self.size - 1 < index + offset:
            raise IndexError(
                "Attempt at indexing an offset that doesn't match the structure provided"
            )
        if offset == 0:
            self._array[index] = value
        else:
            as_bytes = ArrayBuffer.to_bytes(value, offset)
            idx = index
            for i in as_bytes:
                self._array[idx] = i
                idx += 1

    @staticmethod
    def to_bytes(value, length) -> bytearray:
        # always assume big endian
        res = bytearray(length)
        for i in range(length):
            # and with 111111111
            res[i] = value & 0xFF
            # throw away the 8 bytes we just read
            value >>= 8
        if value:
            raise OverflowError(f"Number {value} doesn't fit into {length} bytes")
        return res

    def append(self, value: int):
        self._array.append(value)


@dataclass
class UInt8Array:
    _offset = 1
    _boundary = 255

    def __init__(self, buf: ArrayBuffer):
        self._buffer = buf
        # should we throw an error if not divisible by 8?
        self._size = buf.size // self._offset

    @property
    def buffer(self) -> ArrayBuffer:
        if self._buffer is None:
            raise ValueError("")
        return self._buffer

    @property
    def size(self) -> int:
        return self._size

    # we shouldn't allow for append actually, since the ArrayBuffer is meant to be a static memory store
    def append(self, value: int):
        if value > self._boundary:
            raise SizeException("Value provided isn't supported")
        if value < 0:
            value = (-1 * value) % self._boundary # wrap around the u8 boundary
        self._buffer.append(value)

    def __getitem__(self, index: slice | int) -> Optional[int]:
        bytes = None
        if isinstance(index, slice):
            bytes = self.buffer.__getitem__(index)
        else:
            stop = index+self._offset
            bytes = self.buffer.__getitem__(slice(index, stop, self._offset))
        if bytes is None:
            raise SizeException("Value returned from buffer is nil")
        if isinstance(bytes, int):
            return bytes
        else:
            return int.from_bytes(bytes, byteorder="big", signed=False)

    # switch to using append?
    def __setitem__(self, index: int, value: int):
        if index < 0:
            raise IndexError("ArrayBuffer cannot index negative values")
        if index > self.size - 1:
            raise IndexError("Attempt to index a value larger than size")
        bounded_value = value % 255
        # convert integer into array of bytes
        new_value = [ \
                (bounded_value >> (self._offset*i)) \
                    #                    1 byte per element
                    &0xff for i in range(0,-1,-1) \
                ]

        for idx, val in enumerate(new_value):
            self.buffer[index + idx] = val

    def __repr__(self):
        buf = []
        for i in self._buffer:
            if i is None:
                break
            if isinstance(i, list):
                raise SizeException("Reusing error for impossible case")
            else:
                buf.append(i)
        return f"UInt8Array(buf={buf}, size={self._size})"

# feels pretty similar, can we generalize?
class UInt16Array:
    _offset = 2
    _boundary = 2 ** 16

    def __init__(self, buf: ArrayBuffer):
        self._buffer = buf
        # should we throw an error if not divisible by 8?
        self._size = buf.size // self._offset

    @property
    def buffer(self) -> ArrayBuffer:
        if self._buffer is None:
            raise ValueError("")
        return self._buffer

    @property
    def size(self) -> int:
        return self._size

    # we shouldn't allow for append actually, since the ArrayBuffer is meant to be a static memory store
    def append(self, value: int):
        if value > self._boundary:
            raise SizeException("Value provided isn't supported")
        if value < 0:
            value = (-1 * value) % self._boundary # wrap around the u8 boundary
        self._buffer.append(value)

    def __getitem__(self, index) -> Optional[int]:
        bytes = self.buffer[index:index+self._offset:self._offset]
        if bytes is None:
            raise SizeException("Value returned from buffer is nil")
        if isinstance(bytes, int):
            return bytes
        else:
            return int.from_bytes(bytes, byteorder="big", signed=False)

    # switch to using append?
    def __setitem__(self, index: int, value: int):
        if index < 0:
            raise IndexError("ArrayBuffer cannot index negative values")
        if index > self.size - 1:
            raise IndexError("Attempt to index a value larger than size")
        bounded_value = value % self._boundary
        # if value less than a byte, we only need to process the second member of pair
        #  can we programmatically handle this?
        #  cus this gets messy, imagine handling 64bit doubles :o
        new_value = 0
        if bounded_value < 2 ** 8:
            new_value = bounded_value
            self.buffer[index * self._offset + (self._offset - 1)] = new_value
        else:
            # convert integer into array of bytes when value larger than 1 byte
            new_value = [ \
                    (bounded_value >> (self._offset*i)) \
                        #                    2 bytes per element
                        &0xff for i in range(self._offset - 1,-1,-1) \
                    ]

            for idx, val in enumerate(new_value):
                self.buffer[(index * self._offset) + idx] = val

    def __repr__(self):
        buf = []
        for i in range(0, self._buffer.size, self._offset):
            two_byte_tuple = self._buffer[i:i+2]
            if two_byte_tuple is None:
                break
            if isinstance(two_byte_tuple, list):
                buf.append((two_byte_tuple[0] << 8) + two_byte_tuple[1])
            else:
                raise SizeException("Reusing error for impossible case")
        return f"UInt16Array(buf={buf}, size={self._size})"


arr = ArrayBuffer(8)

u8_arr = UInt8Array(arr)
u8_arr[0] = 2
print(f"u8_arr[0] = 2 => {u8_arr}")
u8_arr[1] = 244
print(f"u8_arr[1] = 244 => {u8_arr}")
u8_arr[2] = 244000
print(f"u8_arr[2] = 244000 => {u8_arr}")

u16_arr = UInt16Array(arr)
print(f"u16_arr => {u16_arr}")
u16_arr[3] = 8
print(f"u16_arr[3] = 8 => {u16_arr}")
print(f"u8_arr => {u8_arr}")
print(f"u16_arr[3] => {u16_arr[3]}")
print(f"u8_arr[6:8] => {u8_arr[6:8]}")

