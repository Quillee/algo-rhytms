"""
To run tests: pytest -m search
"""

from typing import List


def linear_search(haystack: List[int], needle: int) -> bool:
    return bool(
            len(
                list(
                    filter(lambda x: x == needle, haystack))))

