const tst = @import("std").testing;

fn two_crystal_search(breaks: []bool) !usize {
    _ = breaks;
    return error.NoImplFound;
}

// @todo: add more test cases, I guess
test "Search => Two Crystal Search" {
    const VALUES = [_]bool{ false, false, false, false, false, true, true, true, true, true, true };

    var should_skip = two_crystal_search(&VALUES);
    if (should_skip == error.NoImplFound) {
        return error.SkipZigTest;
    }

    tst.expect(two_crystal_search(&VALUES) == 5);
    // tst.expect(two_crystal_search(&VALUES) == -1);
    // tst.expect(two_crystal_search(&VALUES) == 69420);
    // tst.expect(two_crystal_search(&VALUES) == -1);
    // tst.expect(two_crystal_search(&VALUES) == 1);
    // tst.expect(two_crystal_search(&VALUES) == -1);
}
