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


from pytrees.interfaces import Tickable
from pytrees.environment import Environment


class PyTreesState(Tickable):

    def __init__(
        self,
    ) -> None:
        self.environment: Environment = Environment()
        self.ticking = True

    def draw(
        self,
        disp: "PyTreesDisplay"
    ) -> None:
        self.environment.draw(disp)

    def tick(
        self,
    ) -> None:
        if self.ticking:
            self.environment.tick()

    def process_event(
        self,
        event: "PyTreesEvent",
    ) -> None:
        if event == PyTreesEvent.TOGGLE_TICK:
            self.ticking = not self.ticking

from pytrees.display import PyTreesDisplay, PyTreesEvent
