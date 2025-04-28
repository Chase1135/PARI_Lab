import functools
import time

"""Tracks execution times of different functions"""
class Benchmark:
    total_time = 0

    @classmethod
    def get_total_time(cls):
        """Retrieves cumulative execution time for a function"""
        return cls.total_time

    @classmethod
    def reset(cls):
        """Resets all stored execution times"""
        cls.total_time = 0

    @classmethod
    def time_execution(cls, func):
        """Decorator to time function execution and track cumulative time"""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed_time = time.perf_counter() - start_time
            cls.total_time += elapsed_time  # Store cumulative time
            print(f"{func.__name__} executed in {elapsed_time:.6f} seconds", flush=True)
            return result

        return wrapper