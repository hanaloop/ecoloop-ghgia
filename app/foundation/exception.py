import asyncio
import functools
import sys
import traceback

class CatchError:
    def __init__(self, func):
        self.wrapped_func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.wrapped_func):
            return self.async_wrapper(*args, **kwargs)
        else:
            return self.sync_wrapper(*args, **kwargs)

    async def async_wrapper(self, *args, **kwargs):
        try:
            return await self.wrapped_func(*args, **kwargs)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_details = traceback.extract_tb(exc_traceback)[-1]
            filename = tb_details.filename
            line_number = tb_details.lineno
            print(f"An error occurred in function {self.wrapped_func.__name__}: {e} at line {line_number} in file {filename}")

    def sync_wrapper(self, *args, **kwargs):
        try:
            return self.wrapped_func(*args, **kwargs)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_details = traceback.extract_tb(exc_traceback)[-1]
            filename = tb_details.filename
            line_number = tb_details.lineno
            print(f"An error occurred in function {self.wrapped_func.__name__}: {e} at line {line_number} in file {filename}")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return functools.partial(self.__call__, instance)
