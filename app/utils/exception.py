class CustomException(Exception):
    def __init__(self, original_exception: Exception, data = None, ):
        self.data = data
        self.original_exception = original_exception

    def __str__(self):
        return f" \n Error: {self.original_exception.__class__.__name__} at loc: line {self.original_exception.__traceback__.tb_lineno}.\n function: {self.original_exception.__traceback__.tb_frame.f_code.co_name}"
