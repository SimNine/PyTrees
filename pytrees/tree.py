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


from tkinter import Canvas
from typing import Optional

from pytrees.drawable import Drawable
from pytrees.utils import Pos, PyTreeColor


class TreeNode(Drawable):

    RADIUS = 10

    def __init__(
        self,
        pos: Pos,
        owner: "Tree",
        parent: Optional["TreeNode"],
    ) -> None:
        self._parent: Optional[TreeNode] = parent
        self._owner: Tree = owner
        self._pos: Pos = pos

        self._size = self.RADIUS

    def draw(self, canvas: Canvas) -> None:
        canvas.create_oval(
            (self._pos - Pos(TreeNode.RADIUS, TreeNode.RADIUS)).tuple(),
            (self._pos + Pos(TreeNode.RADIUS, TreeNode.RADIUS)).tuple(),
            fill=PyTreeColor.BROWN.value,
        )


class Tree(Drawable):

    def __init__(
        self,
        root: Pos,
    ) -> None:
        self._root = root
        self._root_node = TreeNode(root, self, None)
        self._nodes: list[TreeNode] = [self._root_node]

        self._fitness = 0
        self._nutrients = 0
        self._energy = 0
        self._fitness_percentage = 0

        self._age = 0
        self._topleft = Pos(0, 0)
        self._botright = Pos(0, 0)

    def draw(self, canvas: Canvas) -> None:
        for node in self._nodes:
            node.draw(canvas)
        # canvas.create_oval(
        #     (self._root - Pos(TreeNode.RADIUS, TreeNode.RADIUS)).tuple(),
        #     (self._root + Pos(TreeNode.RADIUS, TreeNode.RADIUS)).tuple(),
        #     fill=PyTreeColor.BROWN.value,
        # )
