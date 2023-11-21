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

from pytrees.utils import Pos, PyTreeColor


class PyTreesDisplay:

    def __init__(self) -> None:
        self._frame_world = tkinter.Tk()
        self._frame_debug = tkinter.Tk()

        # Create canvas
        self._canvas_world = tkinter.Canvas(
            master=self._frame_world,
            bg="white",
            height=600,
            width=600,
            borderwidth=0,
            highlightthickness=0,
        )
        self._canvas_world.pack(
            fill="both",
        )

        self._canvas_debug = tkinter.Canvas(
            master=self._frame_debug,
            bg='white',
            height=200,
            width=400,
            borderwidth=0,
            highlightthickness=0,
        )
        self._canvas_debug.create_rectangle(20, 20, 70, 70, fill=PyTreeColor.YELLOW.value)

        # Register listeners
        self._frame_world.bind("<ButtonPress-1>", self.mouse_left_down)
        self._frame_world.bind("<ButtonRelease-1>", self.mouse_left_release)
        self._frame_world.bind("<B1-Motion>", self.mouse_left_drag)
        self._frame_world.bind("<Configure>", self.resize)
        # self._root.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        # self._root.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        # self._root.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up

        # Show the canvas
        self.update()

    def mouse_left_down(
        self,
        event: tkinter.Event,
    ) -> None:
        self._left_mouse_dragging = False
        self._canvas_world.scan_mark(event.x, event.y)

    def mouse_left_drag(
        self,
        event: tkinter.Event,
    ):
        self._left_mouse_dragging = True
        self._canvas_world.scan_dragto(event.x, event.y, gain=1)

    def mouse_left_release(
        self,
        event: tkinter.Event,
    ):
        if not self._left_mouse_dragging:
            self.last_canvas_click_pos: Pos | None = Pos(
                self._canvas_world.canvasx(event.x),
                self._canvas_world.canvasy(event.y)
            )

    def resize(
        self,
        event: tkinter.Event,
    ):
        self._canvas_world.config(
            width=event.width,
            height=event.height,
        )

    def canvas(
        self,
    ) -> tkinter.Canvas:
        return self._canvas_world

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
    ) -> None:
        self._frame_world.update()
        self._frame_debug.update()

    def clear(
        self,
    ) -> None:
        self._canvas_world.delete("all")
