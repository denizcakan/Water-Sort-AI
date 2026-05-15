# Pure game state management for Water Sort — no pygame dependency.

import copy

from .logic import calc_move, check_victory, generate_level


class GameEngine:
    """Manages Water Sort game state independently of any UI."""

    def __init__(self) -> None:
        self.tube_count: int = 0
        self._tube_colors: list[list[int]] = []
        self._initial_colors: list[list[int]] = []
        self.new_game()

    def get_board(self) -> list[list[int]]:
        """Return a deep copy of the current tube colors."""
        return copy.deepcopy(self._tube_colors)

    def apply_move(self, src: int, dst: int) -> bool:
        """Pour from src into dst. Returns True if the board changed."""
        src_len_before = len(self._tube_colors[src])
        calc_move(self._tube_colors, src, dst)
        return len(self._tube_colors[src]) != src_len_before

    def is_won(self) -> bool:
        """Return True if every tube is empty or fully filled with one color."""
        return check_victory(self._tube_colors)

    def restart(self) -> None:
        """Reset the board to the start of the current level."""
        self._tube_colors = copy.deepcopy(self._initial_colors)

    def new_game(self) -> None:
        """Generate a new random level."""
        self.tube_count, self._tube_colors = generate_level()
        self._initial_colors = copy.deepcopy(self._tube_colors)
