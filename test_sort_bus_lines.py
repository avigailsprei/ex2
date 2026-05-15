import pytest
from sort_bus_lines_wrapper import sort_buses

@pytest.fixture
def sample_buses():
    return [
        {'name': 'a9', 'distance': 500, 'duration': 40, 'frequency': 10},
        {'name': 'z1', 'distance': 100, 'duration': 60, 'frequency': 5},
        {'name': 'b2', 'distance': 900, 'duration': 20, 'frequency': 20},
    ]

def test_sort_by_name(sample_buses):
    sorted_buses = sort_buses(sample_buses, 'name')
    assert len(sorted_buses) == 3
    assert sorted_buses[0]['name'] == 'a9'
    assert sorted_buses[1]['name'] == 'b2'
    assert sorted_buses[2]['name'] == 'z1'

def test_sort_by_distance(sample_buses):
    sorted_buses = sort_buses(sample_buses, 'distance')
    assert len(sorted_buses) == 3
    assert sorted_buses[0]['distance'] == 100
    assert sorted_buses[1]['distance'] == 500
    assert sorted_buses[2]['distance'] == 900

def test_sort_by_duration(sample_buses):
    sorted_buses = sort_buses(sample_buses, 'duration')
    assert len(sorted_buses) == 3
    assert sorted_buses[0]['duration'] == 20
    assert sorted_buses[1]['duration'] == 40
    assert sorted_buses[2]['duration'] == 60

def test_sort_by_frequency(sample_buses):
    sorted_buses = sort_buses(sample_buses, 'frequency')
    assert len(sorted_buses) == 3
    assert sorted_buses[0]['frequency'] == 5
    assert sorted_buses[1]['frequency'] == 10
    assert sorted_buses[2]['frequency'] == 20

def test_empty_list():
    assert sort_buses([], 'name') == []

def test_invalid_sort_type(sample_buses):
    with pytest.raises(ValueError, match="Unknown sort_by type"):
        sort_buses(sample_buses, 'invalid_type')

def test_invalid_bus_data():
    # Bus with uppercase letters is invalid according to C program rules
    invalid_buses = [
        {'name': 'A9', 'distance': 500, 'duration': 40, 'frequency': 10},
    ]
    # The C program prints an error, skips the line, reaches EOF, and prints uninitialized memory (often zeroed).
    result = sort_buses(invalid_buses, 'name')
    assert len(result) == 1
    assert result[0] == {'name': '', 'distance': 0, 'duration': 0, 'frequency': 0}


