import os
import sys
import time
from deprecated import deprecated

@deprecated("Timer is deprecated, use tqdm instead.")
class Timer:
    def __init__(self, total_operations:int) -> None:
        self.total_operations = total_operations
        self.start_time = None
        self.current_operation = 0


    async def __aenter__(self):
        self.start_time = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("All operations completed!")

    async def operation_done(self, clear=True):
        self.current_operation += 1
        elapsed_time = time.time() - self.start_time
        operations_left = self.total_operations - self.current_operation
        avg_time_per_operation = elapsed_time / self.current_operation
        estimated_time_left = operations_left * avg_time_per_operation
        bar_length = 100
        filled_up_length = int(round(bar_length * self.current_operation / self.total_operations))
        percentage = round(100.0 * self.current_operation / self.total_operations, 1)
        bar = '■' * filled_up_length + '-' * (bar_length - filled_up_length)
        if estimated_time_left < 60:
            if clear:
                self.clear()
            print(f"[{bar}] {percentage}% ... \nEstimated time left: {estimated_time_left:.2f} seconds\r")
        elif estimated_time_left < 3600:
            if clear:
                self.clear()
            print(f"[{bar}] {percentage}% ... \nEstimated time left: {estimated_time_left/60:.2f} minutes\r")
        else:
            if clear:
                self.clear()
            print(f"[{bar}] {percentage}% ... \nEstimated time left: {estimated_time_left/3600:.2f} hours\r")

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
