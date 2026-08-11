#Need to move this file once farmework is developed and stable. This is a temporary file to test the timer functionality.

import time


class Timer:

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.perf_counter()
        self.elapsed_ms = (
            self.end_time - self.start_time
        ) * 1000