import asyncio
import functools
import sys
import traceback

def catch_errors_decorator(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            report_error(func, e)

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            report_error(func, e)

    def report_error(f, e):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_details = traceback.extract_tb(exc_traceback)[-1]
        filename = tb_details.filename
        line_number = tb_details.lineno
        print(f"An error occurred in function {f.__name__}: {e} at line {line_number} in file {filename}")
        raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper