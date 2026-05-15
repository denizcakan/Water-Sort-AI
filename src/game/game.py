# Main game class: manages state and runs the event loop for Water Sort.

import copy

import pygame

from .constants import FPS, FONT_PATH, FONT_SIZE, NO_SELECTION, SCREEN_HEIGHT, SCREEN_WIDTH
from .logic import calc_move, check_victory, generate_level
from .renderer import Renderer


class WaterSortGame:
    """Manages game state and runs the main event loop."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Water Sort PyGame")

        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.renderer = Renderer(self.screen, font)
        self.clock = pygame.time.Clock()

        self.tube_count: int = 0
        self.tube_colors: list[list[int]] = []
        self.initial_colors: list[list[int]] = []
        self.tube_rects: list[pygame.Rect] = []

        self.has_selection: bool = False
        self.selected_tube: int = NO_SELECTION
        self.is_won: bool = False
        self.new_game: bool = True

    def _start_new_game(self) -> None:
        """Generate a new level and reset all state."""
        self.tube_count, self.tube_colors = generate_level()
        self.initial_colors = copy.deepcopy(self.tube_colors)
        self.has_selection = False
        self.selected_tube = NO_SELECTION
        self.is_won = False
        self.new_game = False

    def _handle_click(self, pos: tuple[int, int]) -> None:
        """Select a tube on first click, then pour into the destination on second click."""
        for i, rect in enumerate(self.tube_rects):
            if rect.collidepoint(pos):
                if not self.has_selection:
                    self.has_selection = True
                    self.selected_tube = i
                else:
                    self.tube_colors = calc_move(self.tube_colors, self.selected_tube, i)
                    self.has_selection = False
                    self.selected_tube = NO_SELECTION
                break

    def run(self) -> None:
        """Start and run the main game loop until the window is closed."""
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill("black")

            if self.new_game:
                self._start_new_game()

            self.tube_rects = self.renderer.draw_tubes(
                self.tube_count, self.tube_colors, self.selected_tube
            )
            self.is_won = check_victory(self.tube_colors)
            self.renderer.draw_ui(self.is_won)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        # Restart current level from its initial state.
                        self.tube_colors = copy.deepcopy(self.initial_colors)
                        self.has_selection = False
                        self.selected_tube = NO_SELECTION
                    elif event.key == pygame.K_RETURN:
                        self.new_game = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)

            pygame.display.flip()

        pygame.quit()
