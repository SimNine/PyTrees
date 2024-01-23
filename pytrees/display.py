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
    Dims, Pos, PyTreeColor
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

        # Store display state
        self.offset = Pos(0, 0)
        self.debug = False

        # Store mouse state primitives
        self._mouse_buttons_pressed = [False, False, False]
        self._mouse_pos = Pos(0, 0)
        self._mouse_pos_prev = Pos(0, 0)

        # Store most recent mouse click positions
        self.mouse_click_screen = Pos(0, 0)
        self.mouse_click_world = Pos(0, 0)

        # Show the canvas
        self.update()

        # Store misc state
        self.clicked_tree: Optional[Tree] = None

    def process_events(
        self,
        state: "PyTreesState",
    ) -> None:
        # Poll all queue events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_buttons_pressed[0] = True
                self._mouse_pos = self._mouse_pos_prev = Pos(*event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if self._mouse_buttons_pressed[0]:
                    self.offset = self._mouse_pos_prev - Pos(*event.pos) + self.offset
                self._mouse_pos_prev = Pos(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_buttons_pressed[0] = False
                if self._mouse_pos == self._mouse_pos_prev:
                    self.mouse_click_screen = self._mouse_pos
                    self.mouse_click_world = self._mouse_pos + self.offset
                    self._click(state)
                self._mouse_pos = self._mouse_pos_prev = Pos(*event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.debug = not self.debug

    def _click(
        self,
        state: "PyTreesState",
    ) -> None:
        # Check if a tree has been clicked
        for tree in state.environment._trees:
            if tree.bounds.contains(self.mouse_click_world):
                self.clicked_tree = tree
                break

    def draw(
        self,
        state: "PyTreesState",
    ) -> None:
        # Draw the state
        state.draw(self)

        # Draw overlay information
        if self.clicked_tree:
            pygame.draw.rect(
                surface=self.surface,
                color=PyTreeColor.WHITE.value,
                rect=pygame.Rect(
                    Pos(0, 0).tuple(),
                    (
                        self.clicked_tree.bounds.botright -
                        self.clicked_tree.bounds.topleft +
                        Dims(20, 20)
                    ).tuple()
                ),
            )
            self.clicked_tree.draw(
                display=self,
                offset=self.clicked_tree.bounds.topleft - Pos(10, 10),
            )

    @property
    def surface(
        self,
    ) -> pygame.Surface:
        return self._display_surface

    def update(
        self,
    ) -> None:
        pygame.display.flip()

from pytrees.state import PyTreesState
from pytrees.tree import Tree
