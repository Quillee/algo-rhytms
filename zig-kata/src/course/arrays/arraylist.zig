fn ArrayList(comptime T: type) type {
    return struct {
        const Self = @This();

        items: []T,
        len: usize,
        capacity: usize,

        pub fn append(self: Self, item: T) !void {
            _ = item;
            _ = self;
            return error.NoImplFound;
        }

        pub fn get(self: Self, index: usize) !T {
            _ = index;
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

test "Arrays => ArrayList impl" {
    tst.expect(ArrayList(u32) == ArrayList(u32));

    const simple_array = ArrayList(u8){
        // @note: a slice has len, so I'm pretty sure we don't have to store len here
        .items = &[]u8{},
        .len = 0,
        .capacity = 0,
    };

    const should_skip = simple_array.append(255);
    if (should_skip == error.NoImplFound) {
        return error.SkipZigTest;
    }
    // @todo: add test cases
}
