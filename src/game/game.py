# Main game class: manages the pygame event loop and delegates state to GameEngine.

import pygame

from .constants import FPS, FONT_PATH, FONT_SIZE, NO_SELECTION, SCREEN_HEIGHT, SCREEN_WIDTH
from .engine import GameEngine
from .renderer import Renderer


class WaterSortGame:
    """Runs the pygame event loop and wires user input to GameEngine."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Water Sort PyGame")

        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.renderer = Renderer(self.screen, font)
        self.clock = pygame.time.Clock()

        self.engine = GameEngine()
        self.has_selection: bool = False
        self.selected_tube: int = NO_SELECTION
        self.tube_rects: list[pygame.Rect] = []

    def _reset_selection(self) -> None:
        """Clear the current tube selection."""
        self.has_selection = False
        self.selected_tube = NO_SELECTION

    def _handle_click(self, pos: tuple[int, int]) -> None:
        """Select a tube on first click, then pour into destination on second click."""
        for i, rect in enumerate(self.tube_rects):
            if rect.collidepoint(pos):
                if not self.has_selection:
                    self.has_selection = True
                    self.selected_tube = i
                else:
                    self.engine.apply_move(self.selected_tube, i)
                    self._reset_selection()
                break

    def run(self) -> None:
        """Start and run the main game loop until the window is closed."""
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill("black")

            self.tube_rects = self.renderer.draw_tubes(
                self.engine.tube_count, self.engine.get_board(), self.selected_tube
            )
            self.renderer.draw_ui(self.engine.is_won())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.engine.restart()
                        self._reset_selection()
                    elif event.key == pygame.K_RETURN:
                        self.engine.new_game()
                        self._reset_selection()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)

            pygame.display.flip()

        pygame.quit()
