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

from pytrees.display import PyTreesDisplay, PyTreesEvent
from pytrees.state import PyTreesState


def thread_visualize(
    input_queue: "multiprocessing.Queue[PyTreesState]",
    output_queue: "multiprocessing.Queue[PyTreesEvent]",
) -> None:
    display = PyTreesDisplay()
    state: Optional[PyTreesState] = None
    while True:
        try:
            state = input_queue.get(block=False)
        except queue.Empty:
            pass

        try:
            if state is not None:
                display.draw(state)
                events = display.process_events(state)
                for event in events:
                    output_queue.put_nowait(event)
            display.update()
        except Exception as e:
            print(f"Renderer exiting: {e}")
            raise
        # time.sleep(0.05)  # 20 FPS cap


def main():
    state = PyTreesState()

    # Create a queue to push the state onto every tick
    window_input_queue: multiprocessing.Queue[PyTreesState] = multiprocessing.Queue(1)
    window_output_queue: multiprocessing.Queue[PyTreesEvent] = multiprocessing.Queue(20)

    # Create a new thread for rendering
    visualization_process = multiprocessing.Process(
        target=thread_visualize,
        args=[window_input_queue, window_output_queue],
    )
    visualization_process.start()

    # Continually tick the state
    time_curr = time.time()
    num_ticks_this_sec = 0
    while visualization_process.is_alive():
        state.tick()
        try:
            while True:
                try:
                    event = window_output_queue.get(block=False)
                    state.process_event(event)
                except queue.Empty:
                    break

            window_input_queue.put_nowait(state)
        except Exception:
            pass
        tick_end = time.time()
        num_ticks_this_sec += 1
        if tick_end - time_curr >= 1:
            print(f"{num_ticks_this_sec} ticks in {tick_end - time_curr} sec")
            num_ticks_this_sec = 0
            time_curr = tick_end


if __name__ == '__main__':
    main()
