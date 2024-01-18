import pytest

from app.importers.importer_emission_data import EmissionDataImporter



@pytest.fixture
def obj():
    obj = EmissionDataImporter()  # Create an instance of your class here
    obj.adapters = {
        'adapter1': 'adapter1_instance',
        'adapter2': 'adapter2_instance',
        'adapter3': 'adapter3_instance'
    }
    return obj

def test_adapter_found(obj):
    filepath = '/path/to/adapter1/file.txt'
    result = obj.get_adapter_from_file(filepath)
    assert result == 'adapter1_instance'

def test_adapter_not_found(obj):
    filepath = '/path/to/invalid/file.txt'
    result = obj.get_adapter_from_file(filepath)
    assert result is None

def test_adapter_not_found_in_file(obj):
    filepath = '/path/to/adapter4/file.txt'
    result = obj.get_adapter_from_file(filepath)
    assert result is None

def test_import_file(obj):
    filepath = '../../test_data/emission_data.gir1.import.csv'
    result = obj.import_data(filepath)
    assert result
