# Pure game logic for Water Sort — no pygame dependency.

from .constants import TUBE_CAPACITY


def calc_move(
    tube_colors: list[list[int]], src: int, dst: int
) -> list[list[int]]:
    """Pour from src tube into dst tube if the move is valid.

    Moves the longest run of matching colors from the top of src into dst.
    Returns tube_colors unchanged if the move is not possible.
    """
    if not tube_colors[src]:
        return tube_colors

    src_top_color = tube_colors[src][-1]

    # Count consecutive matching colors from the top of src.
    chain_length = 0
    for color in reversed(tube_colors[src]):
        if color == src_top_color:
            chain_length += 1
        else:
            break

    if len(tube_colors[dst]) >= TUBE_CAPACITY:
        return tube_colors

    # An empty dst accepts any color; a non-empty dst requires a color match.
    dst_top_color = tube_colors[dst][-1] if tube_colors[dst] else src_top_color

    if dst_top_color != src_top_color:
        return tube_colors

    for _ in range(chain_length):
        if len(tube_colors[dst]) < TUBE_CAPACITY and tube_colors[src]:
            tube_colors[dst].append(src_top_color)
            tube_colors[src].pop()

    return tube_colors


def check_victory(tube_colors: list[list[int]]) -> bool:
    """Return True if every tube is empty or completely filled with one color."""
    for tube in tube_colors:
        if tube and (len(tube) != TUBE_CAPACITY or len(set(tube)) != 1):
            return False
    return True
