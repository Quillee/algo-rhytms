const tst = @import("std").testing;

fn linear_search(haystack: []i32, needle: i32) !i32 {
    _ = needle;
    _ = haystack;
    return error.NoImplFound;
}

test "Search => Linear Search" {
    const VALUES = [_]i32{ 1, 3, 4, 69, 71, 81, 90, 99, 420, 1337, 69420 };

    var should_skip = linear_search(&VALUES, @as(i32, 1));
    if (should_skip == error.NoImplFound) {
        return error.SkipZigTest;
    }

    tst.expect(linear_search(&VALUES, @as(i32, 69)) == 69);
    tst.expect(linear_search(&VALUES, @as(i32, 1336)) == -1);
    tst.expect(linear_search(&VALUES, @as(i32, 69420)) == 69420);
    tst.expect(linear_search(&VALUES, @as(i32, 69421)) == -1);
    tst.expect(linear_search(&VALUES, @as(i32, 1)) == 1);
    tst.expect(linear_search(&VALUES, @as(i32, 0)) == -1);
}
