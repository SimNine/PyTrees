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


import tkinter

from pytrees.drawable import Drawable
from pytrees.utils import Pos, PyTreeColor


class PyTreesCanvas:

    def __init__(self) -> None:
        self._root = tkinter.Tk()

        # Create canvas
        self._canvas = tkinter.Canvas(
            master=self._root,
            bg="white",
            height=600,
            width=600,
            borderwidth=0,
            highlightthickness=0,
        )
        self._canvas.pack(
            fill="both",
        )

        # Register listeners
        self._root.bind("<ButtonPress-1>", self.mouse_left_down)
        self._root.bind("<ButtonRelease-1>", self.mouse_left_release)
        self._root.bind("<B1-Motion>", self.mouse_left_drag)
        self._root.bind("<Configure>", self.resize)
        # self._root.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        # self._root.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        # self._root.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up

        # Show the canvas
        self._root.update()

    def mouse_left_down(self, event):
        self._left_mouse_dragging = False
        self._canvas.scan_mark(event.x, event.y)

    def mouse_left_drag(self, event):
        self._left_mouse_dragging = True
        self._canvas.scan_dragto(event.x, event.y, gain=1)

    def mouse_left_release(self, event):
        if not self._left_mouse_dragging:
            self._canvas.last_click_pos = Pos(
                self._canvas.canvasx(event.x),
                self._canvas.canvasy(event.y)
            )

    def resize(
        self,
        event: tkinter.Event,
    ):
        self._canvas.config(
            width=event.width,
            height=event.height,
        )

    # def wheel(
    #     self,
    #     event: tkinter.Event,
    # ) -> None:
    #     scale = 1.0
    #     if event.num == 5 or event.delta == -120:  # scroll down
    #         scale /= 2
    #     if event.num == 4 or event.delta == 120:  # scroll up
    #         scale *= 2

    #     self._canvas.scale(
    #         'all',
    #         0, 0,
    #         scale, scale,
    #     )

    def update(
        self,
    ):
        self._canvas.update()

    def clear(
        self,
    ):
        self._canvas.delete("all")

    def draw(
        self,
        item: Drawable,
    ) -> None:
        item.draw(self._canvas)
