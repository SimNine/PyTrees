#############################################################################
# MIT License

# Copyright (c) 2023-2024 Chris Urffer

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#############################################################################


import sys
from typing import Optional

import pygame

from pytrees.utils import (
    Pos, PyTreeColor
)


class PyTreesDisplay:

    def __init__(self) -> None:
        pygame.init()
        self._display_surface = pygame.display.set_mode(
            size=(1200, 700),
            flags=pygame.RESIZABLE,
        )
        self._display_surface.fill(
            color=PyTreeColor.SKY_BLUE.value
        )
        pygame.display.set_caption("Game")
        pygame.display.flip()

        self.offset = Pos(0, 0)
        self.debug = False

        self._mouse_state = [False, False, False]
        self._mouse_pos = (0, 0)
        self._mousedown_pos: Optional[Pos] = None

        # Show the canvas
        self.update()

    def process_events(self) -> None:
        # Poll all queue events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mousedown_pos = Pos(*pygame.mouse.get_pos()) + self.offset
            elif event.type == pygame.MOUSEMOTION:
                if self._mousedown_pos is not None:
                    self.offset = self._mousedown_pos - Pos(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mousedown_pos = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.debug = not self.debug

    @property
    def surface(
        self,
    ) -> pygame.Surface:
        return self._display_surface

    def update(
        self,
    ) -> None:
        pygame.display.flip()
