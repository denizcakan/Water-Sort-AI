# Handles all pygame drawing operations for Water Sort.

import pygame

from .constants import COLOR_CHOICES, NO_SELECTION, SCREEN_WIDTH

# Visual dimensions for a single tube.
_TUBE_WIDTH = 65
_TUBE_HEIGHT = 200
_FILL_STEP = 50  # height of one color block inside a tube


class Renderer:
    """Draws tubes, selection highlights, and UI text onto a pygame surface."""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        self.screen = screen
        self.font = font

    def draw_tubes(
        self,
        tube_count: int,
        tube_colors: list[list[int]],
        selected_tube: int,
    ) -> list[pygame.Rect]:
        """Draw all tubes split into two rows. Returns tube rects for hit-testing."""
        tube_rects: list[pygame.Rect] = []

        if tube_count % 2 == 0:
            tubes_per_row = tube_count // 2
            row_offset = False
        else:
            # Odd count: top row gets one extra, bottom row is shifted right by half a slot.
            tubes_per_row = tube_count // 2 + 1
            row_offset = True

        spacing = SCREEN_WIDTH / tubes_per_row

        # Top row
        for i in range(tubes_per_row):
            x = 5 + spacing * i
            rect = self._draw_tube(i, x, y_fill=200, y_tube=50, tube_colors=tube_colors, selected_tube=selected_tube)
            tube_rects.append(rect)

        # Bottom row
        bottom_count = tubes_per_row - 1 if row_offset else tubes_per_row
        for i in range(bottom_count):
            tube_index = i + tubes_per_row
            x_shift = spacing * 0.5 if row_offset else 0
            x = x_shift + 5 + spacing * i
            rect = self._draw_tube(tube_index, x, y_fill=450, y_tube=300, tube_colors=tube_colors, selected_tube=selected_tube)
            tube_rects.append(rect)

        return tube_rects

    def _draw_tube(
        self,
        tube_index: int,
        x: float,
        y_fill: int,
        y_tube: int,
        tube_colors: list[list[int]],
        selected_tube: int,
    ) -> pygame.Rect:
        """Draw a single tube: fill colors, outline, index label, and selection highlight."""
        tube = tube_colors[tube_index]

        # Fill colors bottom-to-top (index 0 = bottom of tube).
        for j, color_index in enumerate(tube):
            pygame.draw.rect(
                self.screen,
                COLOR_CHOICES[color_index],
                [x, y_fill - _FILL_STEP * j, _TUBE_WIDTH, _FILL_STEP],
                0,
                3,
            )

        # Tube outline.
        rect = pygame.draw.rect(
            self.screen, "blue", [x, y_tube, _TUBE_WIDTH, _TUBE_HEIGHT], 5, 5
        )

        # Index label below the tube.
        label = self.font.render(str(tube_index), True, "white")
        self.screen.blit(label, (rect.centerx - label.get_width() // 2, rect.bottom + 5))

        # Green highlight when this tube is selected.
        if selected_tube == tube_index:
            pygame.draw.rect(
                self.screen, "green", [x, y_tube, _TUBE_WIDTH, _TUBE_HEIGHT], 3, 5
            )

        return rect

    def draw_ui(self, is_won: bool) -> None:
        """Draw the hint bar and, if the player has won, the victory message."""
        hint = self.font.render("Stuck? Space-Restart, Enter-New Board!", True, "white")
        self.screen.blit(hint, (10, 10))

        if is_won:
            victory = self.font.render("You Won! Press Enter for a new board!", True, "white")
            self.screen.blit(victory, (30, 265))
