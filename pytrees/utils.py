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

from pygame import Color, Surface
import pygame


DEBUG = True


class PyTreeColor(Enum):
    SKY_BLUE = "#87CEEB"
    GREEN = "#3BF818"
    YELLOW = "#F8EE18"
    BLUE = "#1756F8"
    BROWN = "#964B00"
    BROWN_LIGHT = "#CC5F3D"
    BLACK = "#000000"
    ORANGE = "#F5A742"
    CLEAR = (255, 255, 255, 255)


class Pos:

    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        self.x = x
        self.y = y

    # Equality
    def __eq__(self, __value: object) -> bool:
        if type(__value) is Pos:
            return self.x == __value.x and self.y == __value.y
        else:
            return False

    # Math
    def __add__(self, __value: 'Pos') -> 'Pos':
        return Pos(self.x + __value.x, self.y + __value.y)

    def __sub__(self, __value: 'Pos') -> 'Pos':
        return Pos(self.x - __value.x, self.y - __value.y)

    def __neg__(self) -> 'Pos':
        return Pos(-self.x, -self.y)

    # Meta
    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    # Conversion
    def tuple(self) -> tuple[int, int]:
        return (self.x, self.y)


Dims = Pos


class Bounds:

    def __init__(
        self,
        topleft: Pos,
        botright: Pos,
    ) -> None:
        self.topleft = topleft
        self.botright = botright

    def contains(
        self,
        point: Pos,
    ) -> bool:
        return (
            self.topleft.y < point.y < self.botright.y and
            self.topleft.x < point.x < self.botright.x
        )


def draw_text(
    surface: Surface,
    left_top: Pos,
    text: str,
    fontsize: int,
    color: PyTreeColor = PyTreeColor.BLACK,
):
    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', fontsize)

    # create a text surface object,
    # on which text is drawn on it.
    text_surface = font.render(text, True, color.value)

    # create a rectangular object for the
    # text surface object
    text_surface_bounds = text_surface.get_rect()

    # set the center of the rectangular object.
    # textRect.center = (X // 2, Y // 2)
    text_surface_bounds.topleft = left_top.tuple()

    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    surface.blit(text_surface, text_surface_bounds)
