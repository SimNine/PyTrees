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


import math
import random
import tkinter
from tkinter import Canvas


from pytrees.drawable import Drawable
from pytrees.utils import Pos, Dims


class Environment(Drawable):

    SKY_BLUE = "#87CEEB"

    WIDTH = 3000
    HEIGHT = 1200

    def __init__(self) -> None:
        self._dims = Dims(self.WIDTH, self.HEIGHT)

        # Create landscape
        gFreq = [
            0.002, 0.01, 0.04, 0.2, 0.5
        ]
        gAmp = [
            random.random()*500,
            random.random()*200,
            random.random()*80,
            random.random()*5,
            random.random()*5
        ]
        gDisp = [
            random.random()*500,
            random.random()*500,
            random.random()*500,
            random.random()*500,
            random.random()*500
        ]
        self._landscape = Landscape(
            dims=self._dims,
            ground_baseline=100,
            ground_freqs=gFreq,
            ground_amps=gAmp,
            ground_disps=gDisp,
        )

        # Create trees
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
            self._dims.tuple(),
            fill=self.SKY_BLUE,
        )

        # Draw landscape
        self._landscape.draw(canvas)

        # Draw trees
        for tree in self._trees:
            tree.draw(canvas)


class Landscape(Drawable):

    def __init__(
        self,
        dims: Dims,
        ground_baseline: int,
        ground_freqs: list[float],
        ground_amps: list[float],
        ground_disps: list[float],
    ) -> None:
        self._dims = dims
        self._ground_baseline = ground_baseline
        self._ground_freqs = ground_freqs
        self._ground_amps = ground_amps
        self._ground_disps = ground_disps

        self._ground_degree = min(
            len(self._ground_freqs),
            len(self._ground_amps),
        )

        self._ground_levels: list[int] = []
        self._populate_ground_levels()

    def draw(self, canvas: Canvas) -> None:
        for i, level in enumerate(self._ground_levels):
            canvas.create_line(
                (i, self._dims.y - level),
                (i, self._dims.y),
                fill=PyTree.BROWN,
            )

    def _populate_ground_levels(self) -> None:
        for x in range(self._dims.x):
            sum: float = 0
            for d in range(self._ground_degree):
                sum += math.cos(
                    self._ground_freqs[d]*x + self._ground_disps[d]
                )*self._ground_amps[d]
                sum += self._ground_baseline
            self._ground_levels.append(sum)


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
