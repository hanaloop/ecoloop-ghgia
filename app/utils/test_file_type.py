import pandas as pd
from app.utils.file_type import return_list


def test_return_list():
    # Define a mock function
    def mock_func(self, data):
        return "Mocked function"

    # Call return_list with the mock function
    decorated_func = return_list(mock_func)

    # Create a mock DataFrame
    data = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})

    # Call the decorated function
    result = decorated_func(None, data)

    # Assert the result
    assert result == "Mocked function"