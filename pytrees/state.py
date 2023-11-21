#############################################################################
# MIT License

# Copyright (c) 2023 Chris Urffer

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
import tkinter
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
        env: Environment
    ) -> None:
        self.environment: Environment = env
        self.last_selected_tree = None

    def draw(
        self,
        disp: PyTreesDisplay
    ) -> None:
        self.environment.draw(disp.canvas())
        disp._canvas_debug.create_rectangle(
            20, 20, 50, 90,
            fill=PyTreeColor.BLUE.value,
        )

        if self.last_selected_tree:
            self.last_selected_tree.draw(disp._canvas_debug)

        if clickpos := disp.last_canvas_click_pos:
            print(f"{clickpos=}")
            for tree in self.environment._trees:
                if tree.bounds.contains(clickpos):
                    # self.last_selected_tree = tree
                    print("TREE MATCH!")
                    disp._canvas_debug.scan_mark(0, 0)
                    disp._canvas_debug.scan_dragto(
                        -tree._root_node._pos.x,
                        -tree._root_node._pos.y,
                        gain=1,
                    )
                    tree.draw(disp._canvas_debug)
                    disp._canvas_debug.scan_mark(0, 0)
                    disp._canvas_debug.scan_dragto(
                        tree._root_node._pos.x,
                        tree._root_node._pos.y,
                        gain=1,
                    )
                    break

    def tick(
        self,
    ) -> None:
        self.environment.tick()
