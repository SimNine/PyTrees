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


from enum import Enum
import math
import random
from typing import Optional

import pygame
from pytrees.display import PyTreesDisplay


from pytrees.interfaces import Drawable, Tickable
from pytrees.environment import Environment
from pytrees.tree import Tree
from pytrees.utils import (
    DEBUG, Pos, Dims, PyTreeColor,
)


class PyTreesState(Tickable):

    def __init__(
        self,
    ) -> None:
        self.environment: Environment = Environment()
        # self.last_selected_tree: Optional[Tree] = None

    def draw(
        self,
        disp: PyTreesDisplay
    ) -> None:
        self.environment.draw(disp)

        # Check if a tree has been clicked
        # TODO: improve this by storing state elsewhere
        for tree in self.environment._trees:
            if tree.bounds.contains(disp.mouse_click_world):
                pygame.draw.rect(
                    surface=disp.surface,
                    color=PyTreeColor.WHITE.value,
                    rect=pygame.Rect(
                        Pos(0, 0).tuple(),
                        (tree.bounds.botright - tree.bounds.topleft + Dims(20, 20)).tuple()
                    ),
                )
                tree.draw(
                    display=disp,
                    offset=tree.bounds.topleft - Pos(10, 10),
                )
                break

    def tick(
        self,
    ) -> None:
        self.environment.tick()
