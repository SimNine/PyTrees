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


import random
import tkinter
from tkinter import Canvas


from pytrees.drawable import Drawable
from pytrees.utils import Pos


class Environment(Drawable):

    SKY_BLUE = "#87CEEB"

    WIDTH = 3000
    HEIGHT = 1500

    def __init__(self) -> None:
        self._dims = (self.WIDTH, self.HEIGHT)

        self._trees: set[PyTree] = set()
        for i in range(100):
            self._trees.add(PyTree(
                Pos(
                    random.randint(0, self.WIDTH),
                    random.randint(0, self.HEIGHT),
                )
            ))

    def draw(self, canvas: Canvas) -> None:
        # Draw background
        canvas.create_rectangle(
            (0, 0),
            self._dims,
            fill=self.SKY_BLUE,
        )

        # Draw trees
        for tree in self._trees:
            tree.draw(canvas)


class PyTree(Drawable):

    RADIUS = 10
    BROWN = "#964B00"

    def __init__(
        self,
        root: Pos,
    ) -> None:
        self._root = root

    def draw(self, canvas: Canvas) -> None:
        canvas.create_oval(
            (self._root - Pos(self.RADIUS, self.RADIUS)).tuple(),
            (self._root + Pos(self.RADIUS, self.RADIUS)).tuple(),
            fill=self.BROWN,
        )
