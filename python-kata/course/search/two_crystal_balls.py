"""
To run tests: pytest -m search
"""

from typing import List
from math import floor, sqrt


"""
walk breaks until false! but then we don't use our other crystal ball
"""
def two_crystal_balls(breaks: List[bool]) -> int:
    jump = floor(sqrt(len(breaks)))
    k = 0

    for i in range(0, len(breaks), jump):
        if breaks[i]:
            break
        k = i

    jmp_slice = breaks[jump:]
    print(f'Mid level state: {jmp_slice} {jump}')

    for i in range(k, len(breaks)):
        if breaks[i]:
            return i 

    # fail state
    return -1


# it is possible to solve that exact problem with logN complexity
# which is better than sqrtN since it grows slower
# https://stackoverflow.com/questions/42038294/is-complexity-ologn-equivalent-to-osqrtn
def two_crystal_balls_logn(breaks: List[bool]) -> int:
    # Note: an optional implementation of the problem with logn time complexity that wasn't even explained in the video
    ...
