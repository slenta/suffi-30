"""Instructions screen: keybindings reference. Any key returns."""

import asyncio
import os
import pygame as pg

from ..config.settings import FPS, TITLE_FONT
from ..core.sound_manager import sound_manager


GAMEPLAY_BINDINGS = [
    ("LEFT / RIGHT", "Move"),
    ("UP", "Jump"),
    ("F", "Shoot"),
    ("G", "Melee (with melee weapon)"),
    ("ESC", "Pause / resume"),
]

MENU_BINDINGS = [
    ("UP / DOWN", "Navigate"),
    ("ENTER / SPACE", "Select"),
    ("ANY KEY", "Back from this screen"),
]


class InstructionsScreen:
    def __init__(self, screen):
        self.screen = screen

        ketchum = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "fonts",
            "Ketchum.otf",
        )
        self.font_title = pg.font.Font(TITLE_FONT, 28)
        self.font_header = pg.font.Font(ketchum, 20)
        self.font_row = pg.font.Font(ketchum, 17)
        self.font_hint = pg.font.Font(ketchum, 18)

        self.bg_color = (128, 0, 128)
        self.title_color = (255, 195, 0)
        self.header_color = (255, 195, 0)
        self.key_color = (100, 220, 200)
        self.desc_color = (220, 220, 220)
        self.hint_color = (200, 200, 200)

    def _draw_section(self, header, bindings, col_left, col_right, y_header, y_first, row_h):
        header_text = self.font_header.render(header, True, self.header_color)
        cx = (col_left + col_right) // 2
        self.screen.blit(header_text, header_text.get_rect(center=(cx, y_header)))

        key_x = col_left
        desc_x = col_left + 160

        for i, (key, desc) in enumerate(bindings):
            y = y_first + i * row_h
            key_text = self.font_row.render(key, True, self.key_color)
            self.screen.blit(key_text, key_text.get_rect(midleft=(key_x, y)))
            desc_text = self.font_row.render(desc, True, self.desc_color)
            self.screen.blit(desc_text, desc_text.get_rect(midleft=(desc_x, y)))

    def _draw(self, title="INSTRUCTIONS", hint="Press any key to return"):
        self.screen.fill(self.bg_color)
        w = self.screen.get_width()
        h = self.screen.get_height()

        title_surf = self.font_title.render(title, True, self.title_color)
        self.screen.blit(title_surf, title_surf.get_rect(center=(w // 2, 28)))

        y_header = 70
        y_first = 104
        row_h = 26

        # Two columns
        left_col_left = 60
        left_col_right = w // 2 - 20
        right_col_left = w // 2 + 20
        right_col_right = w - 60

        self._draw_section(
            "GAMEPLAY",
            GAMEPLAY_BINDINGS,
            left_col_left,
            left_col_right,
            y_header,
            y_first,
            row_h,
        )
        self._draw_section(
            "MENU",
            MENU_BINDINGS,
            right_col_left,
            right_col_right,
            y_header,
            y_first,
            row_h,
        )

        hint_surf = self.font_hint.render(hint, True, self.hint_color)
        self.screen.blit(hint_surf, hint_surf.get_rect(center=(w // 2, h - 18)))

        pg.display.flip()

    async def run(self):
        clock = pg.time.Clock()
        while True:
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "QUIT"
                if event.type == pg.KEYDOWN:
                    sound_manager.play_sound_effect("menu_move")
                    return "BACK"
            self._draw()
            await asyncio.sleep(0)
