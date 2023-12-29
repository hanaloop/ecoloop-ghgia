import argparse
import inspect

def parse_args(func):
    async def wrapper():
        # Get function signature
        signature = inspect.signature(func)
        parameters = list(signature.parameters.values())
        # Create an ArgumentParser
        parser = argparse.ArgumentParser(description=f'Wrapper for {func.__name__}')

        # Add command line arguments dynamically based on function signature
        for param in parameters:
            if param.default != inspect.Parameter.empty:
                arg_type = type(param.default)
                parser.add_argument(f'--{param.name}', type=arg_type, default=param.default, help=f'{param.name} ({arg_type.__name__}), default: {param.default}')
            else:
                parser.add_argument(f'--{param.name}', required=True, help=f'{param.name} (required)')

        # Parse the command line arguments
        args = parser.parse_args()

        # Call the wrapped function with parsed arguments
        await func(**vars(args))

    return wrapper
