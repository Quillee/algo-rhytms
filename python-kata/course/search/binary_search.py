"""
To run tests: pytest -m search
"""

from typing import List

calc_midpoint = lambda lo, hi: (lo + hi) // 2


def binary_search(haystack: List[int], needle: int) -> bool:
    # hay stack should be ordered already
    low = 0
    hi  = len(haystack)

    while hi > low:
        midpoint = calc_midpoint(low, hi)
        if haystack[midpoint]  == needle:
           return True

        if haystack[midpoint] < needle:
            low = midpoint + 1
        else:
            hi = midpoint - 1

    return False


# optional
def recursive_binary_search(haystack: List[int], needle: int) -> bool:
    def recurse(m, hi, lo):
        # fail base case
        if hi < lo:
            return False
        # success base case
        if haystack[m] == needle:
            return True

        if haystack[m] < needle:
            new_lo = m + 1
            return recurse(calc_midpoint(new_lo, hi), hi, new_lo)
        else:
            new_hi = m - 1
            return recurse(calc_midpoint(lo, new_hi), new_hi, lo)

    # starting point
    h = len(haystack) - 1
    l = 0
    return recurse(calc_midpoint(h, l), h, l)

if __name__ == '__main__':
    print('Find 1200, ')
    print([144, 1200, 10000, 29999])
    print(binary_search([144, 1200, 10000, 29999], 1200))
    targets = [
            (1, True),
            (8, False),
            (69, True),
            (1336, False),
            (69420, True),
            (69421, False),
        ]

    haystack = [1, 3, 4, 69, 71, 81, 90, 99, 420, 1337, 69420]
    for target in targets:
        print(target)
        print(f'Iterative => Expected: {target[1]}, Acutal: {binary_search(haystack, target[0])}')
        print(f'Recursive => Expected: {target[1]}, Acutal: {recursive_binary_search(haystack, target[0])}')

