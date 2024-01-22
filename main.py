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


import multiprocessing
import queue
import time
from typing import Optional

from pytrees.display import PyTreesDisplay
from pytrees.state import PyTreesState


def thread_visualize(mp_queue: "multiprocessing.Queue[PyTreesState]") -> None:
    display = PyTreesDisplay()
    state: Optional[PyTreesState] = None
    while True:
        try:
            state = mp_queue.get(block=False)
        except queue.Empty:
            pass

        try:
            # display.clear()
            if state is not None:
                state.draw(display)
            display.process_events()
            display.update()
        except Exception as e:
            print(f"Renderer exiting: {e}")
            raise
        # time.sleep(0.05)  # 20 FPS cap


def main():
    state = PyTreesState()

    # Create a queue to push the state onto every tick
    data_queue: multiprocessing.Queue[PyTreesState] = multiprocessing.Queue(1)

    # Create a new thread for rendering
    visualization_process = multiprocessing.Process(
        target=thread_visualize,
        args=[data_queue],
    )
    visualization_process.start()

    # Continually tick the state
    while visualization_process.is_alive():
        state.tick()
        try:
            data_queue.put_nowait(state)
        except Exception:
            pass
        # time.sleep(0.02)


if __name__ == '__main__':
    main()
