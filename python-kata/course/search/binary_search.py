"""
To run tests: pytest -m search
"""

from typing import List
from math import floor


def binary_search(haystack: List[int], needle: int) -> bool:
    # hay stack should be ordered already
    low = 0
    hi  = len(haystack)
    # | 1 | 2 | 3 | 4 |
    #              lh
    while hi > low:
        midpoint = floor((low + (hi - low)) / 2)
        if haystack[midpoint]  == needle:
           return True

        if haystack[midpoint] < needle:
            low = midpoint + 1
        else:
            hi = midpoint
        print (hi, midpoint, low)

    return False


def recursive_binary_search(haystack: List[int], needle: int) -> bool:
    calc_midpoint = lambda hi, lo: floor(lo + (hi - lo) / 2)
    def recurse(m, hi, lo):
        if haystack[m] == needle:
            return True
        elif hi < lo:
            return False
        elif haystack[m] > needle:
            return recurse(calc_midpoint(hi, lo), hi, m + 1)
        else:
            return recurse(calc_midpoint(hi, lo), m, lo)
    h = len(haystack)
    l = 0
    return recurse(calc_midpoint(h, l), h, l)

