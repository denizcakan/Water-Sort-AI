# Pure game state management for Water Sort — no pygame dependency.

import copy

from .bfs_solver import find_solution
from .logic import calc_move, check_victory, generate_level


class GameEngine:
    """Manages Water Sort game state independently of any UI."""

    def __init__(self) -> None:
        self.tube_count: int = 0
        self._tube_colors: list[list[int]] = []
        self._initial_colors: list[list[int]] = []
        self.solution_moves: list[tuple[int, int]] = []
        self.min_move_count: int = 0
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

    def solve(self) -> list[tuple[int, int]]:
        """Compute and cache the shortest solution from the current board state.

        Updates self.solution_moves and self.min_move_count, and returns the moves.
        """
        self.solution_moves = find_solution(self._tube_colors)
        self.min_move_count = len(self.solution_moves)
        return self.solution_moves

    def restart(self) -> None:
        """Reset the board to the start of the current level."""
        self._tube_colors = copy.deepcopy(self._initial_colors)
        self._clear_solution()

    def new_game(self) -> None:
        """Generate a new random level."""
        self.tube_count, self._tube_colors = generate_level()
        self._initial_colors = copy.deepcopy(self._tube_colors)
        self._clear_solution()

    def _clear_solution(self) -> None:
        """Drop any cached solution so it is recomputed on the next solve() call."""
        self.solution_moves = []
        self.min_move_count = 0
