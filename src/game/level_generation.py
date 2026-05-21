# Deterministic level generation for Water Sort.

import random
from functools import lru_cache
from math import comb, factorial
from typing import NamedTuple, Optional

from .constants import MAX_TUBE_COUNT, MIN_TUBE_COUNT


class LevelKey(NamedTuple):
    """Unique identifier for a level: tube count and position within that tube count's space."""

    tube_count: int
    sequence: int


def valid_level_count(tube_count: int) -> int:
    """Return the total number of valid levels for the given tube count."""
    c = tube_count - 2
    total = 0
    for k in range(c + 1):
        choose_tubes = comb(c, k)
        assign_colors = factorial(c) // factorial(c - k)
        remaining = factorial(4 * (c - k)) // (factorial(4) ** (c - k))
        total += ((-1) ** k) * choose_tubes * assign_colors * remaining
    return total


@lru_cache(None)
def _count_completions(color_number: int, counts: tuple, current_tube: tuple) -> int:
    """Count valid tube arrangements reachable from the current partial state."""
    if sum(counts) == 0:
        return 1

    total = 0
    slot_index = len(current_tube)

    for color in range(color_number):
        if counts[color] == 0:
            continue
        if slot_index == 3 and all(x == color for x in current_tube):
            continue

        new_counts = list(counts)
        new_counts[color] -= 1
        new_tube = () if slot_index == 3 else current_tube + (color,)
        total += _count_completions(color_number, tuple(new_counts), new_tube)

    return total


def generate_from_key(key: LevelKey) -> list:
    """Build tube colors deterministically from a LevelKey."""
    tube_count, sequence = key
    color_number = tube_count - 2
    counts = tuple([4] * color_number)
    total_levels = _count_completions(color_number, counts, ())

    index = (sequence - 1) % total_levels
    flat: list = []
    current_tube: tuple = ()

    while sum(counts) > 0:
        slot_index = len(current_tube)
        for color in range(color_number):
            if counts[color] == 0:
                continue
            if slot_index == 3 and all(x == color for x in current_tube):
                continue

            new_counts = list(counts)
            new_counts[color] -= 1
            new_tube = () if slot_index == 3 else current_tube + (color,)
            branch_count = _count_completions(color_number, tuple(new_counts), new_tube)

            if index >= branch_count:
                index -= branch_count
            else:
                flat.append(color)
                counts = tuple(new_counts)
                current_tube = new_tube
                break

    tubes = [flat[i:i + 4] for i in range(0, len(flat), 4)]
    tubes.append([])
    tubes.append([])
    return tubes


def validate_level_key(key: LevelKey) -> bool:
    """Return True if tube_count is in range and sequence is within bounds."""
    if not (MIN_TUBE_COUNT <= key.tube_count <= MAX_TUBE_COUNT):
        return False
    return 1 <= key.sequence <= valid_level_count(key.tube_count)


def random_level_key() -> LevelKey:
    """Return a LevelKey with randomly chosen tube_count and sequence."""
    tube_count = random.randint(MIN_TUBE_COUNT, MAX_TUBE_COUNT)
    sequence = random.randint(1, valid_level_count(tube_count))
    return LevelKey(tube_count, sequence)
