# BFS solver for Water Sort — finds the shortest sequence of moves that wins the board.

from collections import deque

from .logic import calc_move, check_victory


def find_solution(tube_colors: list[list[int]]) -> list[tuple[int, int]]:
    """Return the shortest list of (src, dst) moves that solves the board.

    Uses breadth-first search over canonical (order-independent) states so that
    symmetric tube arrangements collapse into one. Returns an empty list when the
    board is already solved or no solution exists.
    """
    if check_victory(tube_colors):
        return []

    tube_count = len(tube_colors)
    start = tuple(tuple(tube) for tube in tube_colors)
    start_key = tuple(sorted(start))

    # Queue holds (state, canonical_key) pairs to avoid re-sorting on every pop.
    queue = deque([(start, start_key)])
    # parent[key] = (previous_key, move) — used to reconstruct the move sequence.
    parent = {start_key: (None, None)}

    while queue:
        state, state_key = queue.popleft()

        # Empty tubes are interchangeable: pouring into any of them yields equivalent
        # states, so we only consider the first empty tube as a destination.
        first_empty = next((i for i, tube in enumerate(state) if not tube), None)

        for src in range(tube_count):
            if not state[src]:
                continue
            for dst in range(tube_count):
                if src == dst:
                    continue
                if not state[dst] and dst != first_empty:
                    continue

                # calc_move mutates in place, so apply it to a list copy of the state.
                next_list = [list(tube) for tube in state]
                calc_move(next_list, src, dst)
                next_state = tuple(tuple(tube) for tube in next_list)

                if next_state == state:
                    continue  # Move was invalid or produced no change.

                next_key = tuple(sorted(next_state))
                if next_key in parent:
                    continue

                parent[next_key] = (state_key, (src, dst))

                if check_victory(next_list):
                    return _reconstruct(parent, next_key)

                queue.append((next_state, next_key))

    return []


def _reconstruct(parent: dict, end_key: tuple) -> list[tuple[int, int]]:
    """Walk the parent chain backwards from end_key to recover the move sequence."""
    moves: list[tuple[int, int]] = []
    cur = end_key
    while parent[cur][1] is not None:
        prev_key, move = parent[cur]
        moves.append(move)
        cur = prev_key
    moves.reverse()
    return moves
