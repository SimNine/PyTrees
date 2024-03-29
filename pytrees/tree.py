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
from typing import Optional

import pygame
from pytrees.display import PyTreesDisplay

from pytrees.interfaces import Drawable
import pytrees.mutation
from pytrees.utils import Bounds, Pos, PyTreeColor, draw_text


class TreeNodeType(Enum):
    STRUCT = PyTreeColor.BLACK
    LEAF = PyTreeColor.GREEN
    ROOT = PyTreeColor.BROWN_LIGHT
    WATERCATCHER = PyTreeColor.BLUE


class TreeNode(Drawable):

    def __init__(
        self,
        owner: "Tree",
        parent: Optional["TreeNode"],
        type: Optional[TreeNodeType],
        pos: Optional[Pos],
    ) -> None:
        # Ownership
        self._owner: Tree = owner
        self._parent: Optional[TreeNode] = parent
        self._children: list[TreeNode] = []

        # Type
        if type:
            self._type = type
        else:
            self._type = random.choice(list(TreeNodeType))

        # Position
        if pos:
            self._dist = 0
            self._angle = 0
            self._pos = pos
        else:
            if self._parent is None:
                raise Exception("non-positioned node has no parent")
            self._dist = random.random()*30.0 + pytrees.mutation.MIN_NODE_DISTANCE
            self._angle = math.radians(random.random()*360.0)
            self.update_pos_absolute()

        self._size = int(pytrees.mutation.MIN_NODE_SIZE) * 2

    def add_child(
        self,
        type: TreeNodeType,
    ) -> None:
        self._children.append(TreeNode(
            owner=self._owner,
            parent=self,
            type=type,
            pos=None,
        ))

    def draw(
        self,
        display: PyTreesDisplay,
        offset: Optional[Pos] = None,
    ) -> None:
        if offset is None:
            offset = display.offset

        pygame.draw.circle(
            surface=display.surface,
            color=self._type.value.value,
            center=(self._pos - offset).tuple(),
            radius=self._size,
        )
        if display.debug:
            pygame.draw.rect(
                surface=display.surface,
                color=PyTreeColor.BLACK.value,
                rect=pygame.Rect(
                    (self._pos - Pos(self._size, self._size) - offset).tuple(),
                    Pos(self._size*2, self._size*2).tuple(),
                ),
                width=1,
            )

    def draw_recursive(
        self,
        display: PyTreesDisplay,
        offset: Optional[Pos] = None,
    ) -> None:
        if offset is None:
            offset = display.offset

        for child in self._children:
            pygame.draw.line(
                surface=display.surface,
                color=PyTreeColor.BLACK.value,
                start_pos=(self._pos - offset).tuple(),
                end_pos=(child._pos - offset).tuple(),
            )
            child.draw_recursive(display, offset)
        self.draw(display, offset)

    @classmethod
    def clone(
        cls,
        node: "TreeNode",
        owner: Optional["Tree"],
        parent: Optional["TreeNode"],
        type: Optional[TreeNodeType],
        pos: Optional[Pos],
    ) -> "TreeNode":
        return cls(
            owner=(owner if owner else node._owner),
            parent=(parent if parent else node._parent),
            type=(type if type else node._type),
            pos=(pos if pos else node._pos),
        )

    def update_pos_absolute(
        self,
    ) -> None:
        if self._parent is None:
            return
        self._pos = self._parent._pos + Pos(
            int(math.sin(self._angle)*self._dist),
            int(math.cos(self._angle)*self._dist),
        )

    def contains(
        self,
        pos: Pos,
    ) -> bool:
        delta = pos - self._pos
        dist = math.sqrt(delta.x**2 + delta.y**2)
        return dist < self._size

    def get_pos_extremes(
        self,
    ) -> tuple[Pos, Pos]:
        topleft = self._pos - Pos(self._size, self._size)
        bottomright = self._pos + Pos(self._size, self._size)
        for child in self._children:
            child_topleft, child_bottomright = child.get_pos_extremes()
            if child_topleft.x < topleft.x:
                topleft.x = child_topleft.x
            if child_topleft.y < topleft.y:
                topleft.y = child_topleft.y
            if child_bottomright.x > bottomright.x:
                bottomright.x = child_bottomright.x
            if child_bottomright.y > bottomright.y:
                bottomright.y = child_bottomright.y
        return (topleft, bottomright)

    def get_children_recursively(
        self,
    ) -> set["TreeNode"]:
        ret: set["TreeNode"] = {self}
        for child in self._children:
            ret.update(child.get_children_recursively())
        return ret

    def mutate(self):
        # Chance of changing this node's type
        if random.random() < pytrees.mutation.CHANCE_NODE_TYPE:
            new_type = random.choice(list(TreeNodeType))

            # re-roll, to make it more likely that the root node is a struct node
            if (
                new_type is not TreeNodeType.STRUCT and
                random.random() < pytrees.mutation.CHANCE_NODE_TYPE_STRUCT
            ):
                new_type = random.choice(list(TreeNodeType))

            # if the new type is not a struct, remove all children
            if new_type is not TreeNodeType.STRUCT:
                self._children.clear()

            # set the new type
            self._type = new_type

        # Chance of mutating this node's size
        if random.random() < pytrees.mutation.CHANCE_NODE_SIZE:
            size_inc = int(random.random() * 20.0 - 10.0)
            self._size += size_inc
            if self._size < pytrees.mutation.MIN_NODE_SIZE:
                self._size = pytrees.mutation.MIN_NODE_SIZE

        # For each child, chance of losing it. If not lost, mutate it
        remaining_children: list[TreeNode] = []
        for child in self._children:
            if random.random() > pytrees.mutation.CHANCE_NODE_DELETE:
                remaining_children.append(child)
                child.mutate()
        self._children = remaining_children

        # Chance of adding child nodes, if this is a structure node
        while (
            self._type is TreeNodeType.STRUCT and
            random.random() < pytrees.mutation.CHANCE_NODE_ADD
        ):
            self.add_child(random.choice(list(TreeNodeType)))

        # Chance to mutate angle between this node and its parent
        if random.random() < pytrees.mutation.CHANCE_NODE_ANGLE:
            angle_inc = random.random() * 30.0 - 15
            self._angle += angle_inc
            self.update_pos_absolute()

        # Chance of changing this node's distance from its parent
        if random.random() < pytrees.mutation.CHANCE_NODE_DISTANCE:
            distInc = random.random() * 30.0 - 15
            self._dist += distInc

            # Check for minimum distance
            if self._dist < pytrees.mutation.MIN_NODE_DISTANCE:
                self._dist = pytrees.mutation.MIN_NODE_DISTANCE

            self.update_pos_absolute()


class Tree(Drawable):

    def __init__(
        self,
        root: Pos,
    ) -> None:
        self._fitness = 0
        self._nutrients = 0
        self._energy = 0
        self._fitness_percentage = 0

        self._age = 0

        self._root_node = TreeNode(
            owner=self,
            parent=None,
            type=TreeNodeType.STRUCT,
            pos=root,
        )
        self._root_node.mutate()

        self.bounds = Bounds(*self._root_node.get_pos_extremes())
        self._nodes: set[TreeNode] = self._root_node.get_children_recursively()

    def draw(
        self,
        display: PyTreesDisplay,
        offset: Optional[Pos] = None,
    ) -> None:
        if offset is None:
            offset = display.offset

        self._root_node.draw_recursive(display, offset)
        if display.debug:
            pygame.draw.rect(
                surface=display.surface,
                color=PyTreeColor.BLACK.value,
                rect=pygame.Rect(
                    (self.bounds.topleft - offset).tuple(),
                    (self.bounds.botright - self.bounds.topleft).tuple(),
                ),
                width=1,
            )
            draw_text(
                surface=display.surface,
                left_top=(self.bounds.topleft - offset),
                text=str(self._energy),
                fontsize=10,
            )
