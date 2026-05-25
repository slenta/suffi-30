"""Highscore screen: top 5 per level, columns side-by-side. Any key returns."""

import asyncio
import os
import pygame as pg

from ..config.settings import FPS, TITLE_FONT
from ..core.sound_manager import sound_manager


LEVELS = ["baby-level", "graffiti", "hospital", "trancefloor"]


class HighscoreScreen:
    def __init__(self, screen, highscore_manager):
        self.screen = screen
        self.manager = highscore_manager

        ketchum = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "fonts",
            "Ketchum.otf",
        )
        self.font_title = pg.font.Font(TITLE_FONT, 36)
        self.font_header = pg.font.Font(ketchum, 18)
        self.font_row = pg.font.Font(ketchum, 14)
        self.font_hint = pg.font.Font(ketchum, 16)

        # Match level-selection screen background
        self.bg_color = (128, 0, 128)
        self.title_color = (255, 195, 0)
        self.header_color = (255, 195, 0)
        self.text_color = (220, 220, 220)
        self.hint_color = (200, 200, 200)

        self.scores = {lvl: None for lvl in LEVELS}

    async def _load(self):
        async def fetch(level):
            try:
                result = self.manager.get_top_scores(level, limit=5)
                if asyncio.iscoroutine(result):
                    result = await result
                self.scores[level] = result or []
            except Exception as e:
                print(f"⚠️ HighscoreScreen: failed to load {level}: {e}")
                self.scores[level] = []

        await asyncio.gather(*(fetch(lvl) for lvl in LEVELS))

    def _display_name(self, level):
        return level.replace("-", " ").upper()

    def _draw(self):
        self.screen.fill(self.bg_color)
        w = self.screen.get_width()
        h = self.screen.get_height()

        # Title with breathing room above and below
        title = self.font_title.render("HIGHSCORES", True, self.title_color)
        self.screen.blit(title, title.get_rect(center=(w // 2, 35)))

        col_w = w // len(LEVELS)
        y_header = 90
        y_first = 125
        row_h = 22
        pad = 8

        for i, level in enumerate(LEVELS):
            col_left = col_w * i + pad
            col_right = col_w * (i + 1) - pad
            cx = col_w * i + col_w // 2

            header = self.font_header.render(
                self._display_name(level), True, self.header_color
            )
            self.screen.blit(header, header.get_rect(center=(cx, y_header)))

            scores = self.scores[level]
            if scores is None:
                msg = self.font_row.render("Loading...", True, self.text_color)
                self.screen.blit(msg, msg.get_rect(center=(cx, y_first + row_h)))
                continue
            if not scores:
                msg = self.font_row.render("(no scores)", True, self.text_color)
                self.screen.blit(msg, msg.get_rect(center=(cx, y_first + row_h)))
                continue

            for rank, entry in enumerate(scores[:5]):
                y = y_first + rank * row_h
                name = (entry.get("player_name") or "?")[:15]
                score = (
                    entry.get("score")
                    or entry.get("breakdown", {}).get("total_score")
                    or 0
                )

                # Render rank+name on the left, score on the right of the column
                left_text = self.font_row.render(
                    f"{rank + 1}. {name}", True, self.text_color
                )
                self.screen.blit(left_text, left_text.get_rect(midleft=(col_left, y)))

                score_text = self.font_row.render(
                    str(score), True, self.text_color
                )
                self.screen.blit(
                    score_text, score_text.get_rect(midright=(col_right, y))
                )

        hint = self.font_hint.render(
            "Press any key to return", True, self.hint_color
        )
        self.screen.blit(hint, hint.get_rect(center=(w // 2, h - 18)))

        pg.display.flip()

    async def run(self):
        clock = pg.time.Clock()
        load_task = asyncio.create_task(self._load())
        try:
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
        finally:
            if not load_task.done():
                load_task.cancel()
