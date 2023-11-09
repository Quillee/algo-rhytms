from sys import getsizeof
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
import array
from typing import MutableSequence, Optional, TypeVar, List


class SizeException(TypeError):
    def __init__(self, *args, **kwargs):
        super(SizeException, self).__init__(args, kwargs)


arr = array.array("b")


class DogBreed(Enum):
    DOBERMAN = "doberman"
    DASCHUND = "daschund"
    BEAGLE = "beagle"


# how would I create a ArrayBuffer[Dog] for my dog adoption app?


@dataclass
class Dog:
    name: str
    breed: DogBreed
    date_released: datetime
    date_adopted: datetime


@dataclass
class ArrayBuffer:
    _array: bytearray

    def __init__(self, size: int):
        self._size = size
        self._array = bytearray()

    @property
    def size(self) -> int:
        return self.size

    def __getitem__(self, index: int, offset: int = 0) -> Optional[bytearray]:
        if index > self._size - 1:
            return None
        return self._array[index : index + offset]

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
    def __init__(self, buf: ArrayBuffer[int]):
        self._buffer = buf
        # should we throw an error if not divisible by 8?
        self._size = buf.size // 8

    @property
    def buffer(self) -> ArrayBuffer[int]:
        if self._buffer is None:
            raise ValueError("")
        return self._buffer

    @property
    def size(self) -> int:
        return self._size

    def append(self, value: int):
        if value > 256:
            raise SizeException("Value provided isn't supported")
        if value < 0:
            value = (-1 * value) % 256  # wrap around the u8 boundary
        self._buffer.append(value)

    def __getitem__(self, index) -> Optional[int]:
        bytes = self.buffer.__getitem__(index, 0)
        if bytes is None:
            raise SizeException("Value returned from buffer is nil")
        return int.from_bytes(bytes, byteorder="big", signed=False)

    # switch to using append?
    def __setitem__(self, index: int, value: int):
        if index < 0:
            raise IndexError("ArrayBuffer cannot index negative values")
        if index - 1 > self.size:
            raise IndexError("Attempt to index a value larger than size")
        # self._array[index] = value


arr = ArrayBuffer(8)

u8_arr = UInt8Array(arr)
print(u8_arr)
