from src import utils


class TestGroupedDict:
    # Tests that the function correctly groups a list of dictionaries by a valid key
    def test_happy_path(self):
        input_list = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 25},
        ]
        expected_output = {
            25: [{"name": "Alice", "age": 25}, {"name": "Charlie", "age": 25}],
            30: [{"name": "Bob", "age": 30}],
        }
        assert utils.grouped_dict(input_list, "age") == expected_output

    # Tests that the function returns an empty dictionary when given an empty list
    def test_empty_list(self):
        input_list = []
        expected_output = {}
        assert utils.grouped_dict(input_list, "age") == expected_output

    # Tests that the function correctly handles dictionaries with missing keys
    def test_missing_keys(self):
        input_list = [
            {"name": "Alice", "age": 25},
            {"name": "Bob"},
            {"name": "Charlie", "age": 25},
        ]
        expected_output = {
            25: [{"name": "Alice", "age": 25}, {"name": "Charlie", "age": 25}]
        }
        assert utils.grouped_dict(input_list, "age") == expected_output

    # Tests that the function correctly handles dictionaries with duplicate keys
    def test_duplicate_keys(self):
        input_list = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 25},
            {"name": "Dave", "age": 30},
        ]
        expected_output = {
            25: [{"name": "Alice", "age": 25}, {"name": "Charlie", "age": 25}],
            30: [{"name": "Bob", "age": 30}, {"name": "Dave", "age": 30}],
        }
        assert utils.grouped_dict(input_list, "age") == expected_output

    # Tests that the function correctly handles dictionaries with nested values
    def test_nested_values(self):
        input_list = [
            {
                "name": "Alice",
                "age": 25,
                "address": {"city": "New York", "state": "NY"},
            },
            {
                "name": "Bob",
                "age": 30,
                "address": {"city": "San Francisco", "state": "CA"},
            },
            {
                "name": "Charlie",
                "age": 25,
                "address": {"city": "New York", "state": "NY"},
            },
        ]
        expected_output = {
            25: [
                {
                    "name": "Alice",
                    "age": 25,
                    "address": {"city": "New York", "state": "NY"},
                },
                {
                    "name": "Charlie",
                    "age": 25,
                    "address": {"city": "New York", "state": "NY"},
                },
            ],
            30: [
                {
                    "name": "Bob",
                    "age": 30,
                    "address": {"city": "San Francisco", "state": "CA"},
                }
            ],
        }
        assert utils.grouped_dict(input_list, "age") == expected_output
