const tst = @import("std").testing;

fn bubble_sort(arr: []i32) ![]i32 {
    _ = arr;
    return error.NoImplFound;
}

test "Search => Bubble Sort" {
    const arr_unsorted = [_]u8{ 9, 3, 7, 4, 69, 420, 42 };
    const arr_sorted = [_]u8{ 3, 4, 7, 9, 42, 69, 420 };

    var should_skip = bubble_sort([_]i64{ 3, 2, 1 });
    if (should_skip == error.NoImplFound) {
        return error.SkipZigTest;
    }

    // @todo: test that == works here
    tst.expect(bubble_sort(arr_unsorted) == arr_sorted);
}
