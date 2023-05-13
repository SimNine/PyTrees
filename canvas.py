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


class PyTreesCanvas:

    def __init__(self) -> None:
        self._root = tkinter.Tk()

        # Create canvas
        self._canvas = tkinter.Canvas(
            master=self._root,
            bg="white",
            height=300,
            width=300,
            borderwidth=0,
            highlightthickness=0,
        )
        self._canvas.pack(
            fill="both",
        )

        # Register listeners
        self._root.bind("<ButtonPress-1>", self.scroll_start)
        self._root.bind("<B1-Motion>", self.scroll_move)
        self._root.bind("<Configure>", self.resize)

        # Show the canvas
        self._root.update()

    def scroll_start(self, event):
        self._canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self._canvas.scan_dragto(event.x, event.y, gain=1)

    def resize(
        self,
        event: tkinter.Event,
    ):
        self._canvas.config(
            width=event.width,
            height=event.height,
        )

    def draw_arcs(
        self,
        topleft=(10, 10),
    ):
        # Draw arcs
        bottomright = (topleft[0] + 280, topleft[1] + 280)
        coords = topleft + bottomright
        self._canvas.create_arc(coords, start=0, extent=150, fill="red")
        self._canvas.create_arc(coords, start=150, extent=210, fill="green")

    def update(
        self,
    ):
        self._canvas.update()

    def clear(
        self,
    ):
        self._canvas.delete("all")
