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
import tkinter
from pytrees.display import PyTreesDisplay


from pytrees.interfaces import Drawable
from pytrees.tree import Tree
from pytrees.utils import (
    DEBUG, Pos, Dims, PyTreeColor,
)


class ParticleType(Enum):
    SUN = 0
    WATER = 1


class Environment(Drawable):

    WIDTH = 3000
    HEIGHT = 1200

    NUM_TREES_STARTING = 200
    NUM_WARMUP_TICKS = 1000

    def __init__(self) -> None:
        self._dims = Dims(self.WIDTH, self.HEIGHT)

        self._trees: set[Tree] = set()

        self._particles_sun: set[Particle] = set()
        self._particles_water: set[Particle] = set()

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

        # Create initial particles
        self._warmup(self.NUM_WARMUP_TICKS)

        # Create trees
        for _ in range(self.NUM_TREES_STARTING):
            x_pos = random.randint(0, self.WIDTH)
            self._trees.add(Tree(
                Pos(
                    x_pos,
                    self._landscape._ground_levels[x_pos],
                )
            ))

    def _warmup(
        self,
        num_ticks: int,
    ) -> None:
        for _ in range(num_ticks):
            self.tick()

    def _add_new_particles(
        self,
        num_particles: int,
        type: ParticleType,
    ) -> None:
        for _ in range(num_particles):
            if type is ParticleType.SUN:
                self._particles_sun.add(ParticleSun(
                    random.randint(0, self.WIDTH),
                    0,
                ))
            elif type is ParticleType.WATER:
                self._particles_water.add(ParticleRain(
                    random.randint(0, self.WIDTH),
                    0,
                ))

    def draw(self, canvas: tkinter.Canvas) -> None:
        # Draw background
        canvas.create_rectangle(
            (0, 0),
            self._dims.tuple(),
            fill=PyTreeColor.SKY_BLUE.value,
        )

        # Draw landscape
        self._landscape.draw(canvas)

        # Draw trees
        for tree in self._trees:
            tree.draw(canvas)

        # Draw sun particles
        for particle_sun in self._particles_sun:
            particle_sun.draw(canvas)

        # Draw water particles
        for particle_water in self._particles_water:
            particle_water.draw(canvas)

    def tick(self) -> None:
        self._add_new_particles(2, ParticleType.SUN)
        self._add_new_particles(2, ParticleType.WATER)
        for p in self._particles_sun:
            p.tick()
        for p in self._particles_water:
            p.tick()
        self._particles_sun = self._collide_particles_with_landscape(self._particles_sun)
        self._particles_water = self._collide_particles_with_landscape(self._particles_water)
        self._particles_sun = self._collide_particles_with_trees(self._particles_sun)
        self._particles_water = self._collide_particles_with_trees(self._particles_water)

    def _collide_particles_with_landscape(
        self,
        particles: set["Particle"],
    ) -> set["Particle"]:
        ret: set[Particle] = set()
        for particle in particles:
            if not self._landscape.is_pos_ground(particle):
                ret.add(particle)
        return ret

    def _collide_particles_with_trees(
        self,
        particles: set["Particle"],
    ) -> set["Particle"]:
        for particle in particles:
            for tree in self._trees:
                if tree.bounds.contains(particle):
                    for node in tree._nodes:
                        if node.contains(particle):
                            particle.spent = True
                            tree._energy += particle.power
                            break
                    if particle.spent:
                        break

        return {
            particle
            for particle in particles
            if not particle.spent
        }


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

    def draw(self, canvas: tkinter.Canvas) -> None:
        for i, level in enumerate(self._ground_levels):
            canvas.create_line(
                (i, level),
                (i, self._dims.y),
                fill=PyTreeColor.BROWN.value,
            )

    def _populate_ground_levels(self) -> None:
        for x in range(self._dims.x):
            sum: float = 0
            for d in range(self._ground_degree):
                sum += int(math.cos(
                    self._ground_freqs[d]*x + self._ground_disps[d]
                )*self._ground_amps[d])
                sum += self._ground_baseline
            self._ground_levels.append(sum)

    def is_pos_ground(self, pos: Pos) -> bool:
        if (
            pos.x < 0 or pos.x >= self._dims.x or
            pos.y < 0 or pos.y >= self._dims.y
        ):
            return False
        if self._ground_levels[pos.x] <= pos.y:
            return True
        else:
            return False


class Particle(Pos, Drawable):

    def __init__(
        self,
        x: int, y: int,
        color: str,
        power: int,
    ) -> None:
        super().__init__(x, y)
        self._color = color
        self.spent = False
        self.power = power

    def draw(
        self,
        canvas: tkinter.Canvas,
    ) -> None:
        canvas.create_rectangle(
            self.x - 2, self.y - 2,
            self.x + 2, self.y + 2,
            fill=self._color,
        )
        if DEBUG:
            canvas.create_text(
                self.tuple(),
                fill=PyTreeColor.BLACK.value,
                text=str(self.power),
            )

    def tick(
        self,
    ) -> None:
        self.y += 1


class ParticleSun(Particle):

    POWER_BASE = 70000
    POWER_INC_PER_TICK = -45

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, PyTreeColor.YELLOW.value, self.POWER_BASE)

    def tick(self) -> None:
        self.power += self.POWER_INC_PER_TICK
        return super().tick()


class ParticleRain(Particle):

    POWER_BASE = -50000
    POWER_INC_PER_TICK = 55

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, PyTreeColor.BLUE.value, self.POWER_BASE)

    def tick(self) -> None:
        self.power += self.POWER_INC_PER_TICK
        return super().tick()
