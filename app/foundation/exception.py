import asyncio
import functools

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
            print(f"An error occurred in async function {self.wrapped_func.__name__}: {e} at line {e.__traceback__.tb_lineno}")

    def sync_wrapper(self, *args, **kwargs):
        try:
            return self.wrapped_func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred in function {self.wrapped_func.__name__}: {e} at line {e.__traceback__.tb_lineno}")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return functools.partial(self.__call__, instance)
