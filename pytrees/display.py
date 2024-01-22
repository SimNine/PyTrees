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


import sys
from typing import Optional

import pygame

from pytrees.utils import (
    Pos, PyTreeColor
)


class PyTreesDisplay:

    def __init__(self) -> None:
        # self._frame_world = tkinter.Tk()
        # self._frame_debug = tkinter.Tk()

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
        self._mouse_state = [False, False, False]
        self._mouse_pos = (0, 0)
        self._mousedown_pos: Optional[Pos] = None

        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()

        # Create canvas
        # self._canvas_world = tkinter.Canvas(
        #     master=self._frame_world,
        #     bg="white",
        #     height=600,
        #     width=600,
        #     borderwidth=0,
        #     highlightthickness=0,
        # )
        # self._canvas_world.pack(
        #     fill="both",
        # )
        # self.last_canvas_click_pos = None

        # self._canvas_debug = tkinter.Canvas(
        #     master=self._frame_debug,
        #     bg='white',
        #     height=200,
        #     width=400,
        #     borderwidth=0,
        #     highlightthickness=0,
        # )
        # self._canvas_debug.pack(
        #     fill="both",
        # )
        # self._canvas_debug.create_rectangle(20, 20, 70, 70, fill=PyTreeColor.YELLOW.value)

        # Register listeners
        # self._frame_world.bind("<ButtonPress-1>", self.mouse_left_down)
        # self._frame_world.bind("<ButtonRelease-1>", self.mouse_left_release)
        # self._frame_world.bind("<B1-Motion>", self.mouse_left_drag)
        # self._frame_world.bind("<Configure>", self.world_resize)
        # self._frame_debug.bind("<Configure>", self.debug_resize)
        # self._root.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        # self._root.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        # self._root.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up

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

        # Get new mouse state
        mouse_state_new = pygame.mouse.get_pressed()

        # Check for mouse button state changes
        if (
            self._mouse_state[0] is False and
            mouse_state_new[0] is True
        ):
            # Left click
            pass
            # self._canvas_world.scan_mark(event.x, event.y)
        elif (
            self._mouse_state[0] is True and
            mouse_state_new[0] is True
        ):
            # Mouse drag
            pass
            # self._left_mouse_dragging = True
            # self._canvas_world.scan_dragto(event.x, event.y, gain=1)
        elif (
            self._mouse_state is True and
            mouse_state_new[0] is False
        ):
            # Mouse release
            pass
            # if not self._left_mouse_dragging:
            #     self.last_canvas_click_pos: Pos | None = Pos(
            #         self._canvas_world.canvasx(event.x),
            #         self._canvas_world.canvasy(event.y)
            #     )
            # self._left_mouse_dragging = False

        # Refresh mouse state
        self._mouse_state = mouse_state_new
        # self._mouse_pos = mouse_pos_new

    # def world_resize(
    #     self,
    #     event: tkinter.Event,
    # ):
    #     self._canvas_world.config(
    #         width=event.width,
    #         height=event.height,
    #     )

    # def debug_resize(
    #     self,
    #     event: tkinter.Event,
    # ):
    #     self._canvas_debug.config(
    #         width=event.width,
    #         height=event.height,
    #     )

    @property
    def surface(
        self,
    ) -> pygame.Surface:
        return self._display_surface

    # def canvas_world(
    #     self,
    # ) -> tkinter.Canvas:
    #     return self._canvas_world

    # def canvas_debug(
    #     self,
    # ) -> tkinter.Canvas:
    #     return self._canvas_debug

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
        pygame.display.flip()
        # self._frame_world.update()
        # self._frame_debug.update()

    def clear(
        self,
    ) -> None:
        return
        self._canvas_world.delete("all")
        self._canvas_debug.delete("all")
