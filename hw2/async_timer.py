import asyncio
from time import perf_counter


class AsyncTimer:
    def __init__(self, label=""):
        self.label = label
        self.start_time = None
        self.duration = None
    
    async def __aenter__(self):
        self.start_time = perf_counter()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is not None:
            self.duration = perf_counter() - self.start_time
            label_str = f" ({self.label})" if self.label else ""
            print(f"Время выполнения{label_str}: {self.duration:.4f} секунд")

