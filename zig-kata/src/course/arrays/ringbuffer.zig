fn RingBuffer(comptime T: type) type {
    return struct {
        const Self = @This();

        items: []T,
        cap: usize,

        pub fn push(self: Self, item: T) !void {
            _ = item;
            _ = self;
            return error.NoImplFound;
        }

        pub fn pop(self: Self) !T {
            _ = self;
            return error.NoImplFound;
        }

        pub fn set(self: Self, value: T) !void {
            _ = value;
            _ = self;
            return error.NoImplFound;
        }
    };
}

const tst = @import("std").testing;

test "Arrays => RingBuffer impl" {
    tst.expect(RingBuffer(u32) == RingBuffer(u32));

    const simple_array = RingBuffer(u8){
        .items = &[]u8{},
        .capacity = 0,
    };

    const should_skip = simple_array.append(255);
    if (should_skip == error.NoImplFound) {
        return error.SkipZigTest;
    }
    // @todo: add test cases
}
