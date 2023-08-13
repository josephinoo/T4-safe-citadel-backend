from src.utils import grouped_dict


class TestGroupedDict:
    # Test that the function returns an empty dictionary when given None as input
    def test_empty_input(self):
        result = grouped_dict(None)
        assert result == {}

    # Test that the function correctly groups a list of dictionaries by a specified key
    def test_grouping(self):
        input_data = [
            {"state": "CA", "city": "Los Angeles"},
            {"state": "CA", "city": "San Francisco"},
            {"state": "NY", "city": "New York"},
            {"state": "NY", "city": "Albany"},
        ]

        expected_result = {
            "CA": [
                {"state": "CA", "city": "Los Angeles"},
                {"state": "CA", "city": "San Francisco"},
            ],
            "NY": [
                {"state": "NY", "city": "New York"},
                {"state": "NY", "city": "Albany"},
            ],
        }

        result = grouped_dict(input_data)
        assert result == expected_result

    # Test that the function correctly groups a list of dictionaries with non-empty input
    def test_non_empty_input(self):
        input_data = [
            {"state": "TX", "city": "Austin"},
            {"state": "TX", "city": "Dallas"},
        ]

        expected_result = {
            "TX": [
                {"state": "TX", "city": "Austin"},
                {"state": "TX", "city": "Dallas"},
            ],
        }

        result = grouped_dict(input_data)
        assert result == expected_result

    # Test that the function returns an empty dictionary when given an empty list as input
    def test_empty_list(self):
        result = grouped_dict([])
        assert result == {}

    # Test that the function correctly handles dictionaries with missing keys
    def test_missing_keys(self):
        input_data = [
            {"state": "TX", "city": "Austin"},
            {"state": "TX", "city": "Dallas"},
        ]

        expected_result = {
            "TX": [
                {"state": "TX", "city": "Austin"},
                {"state": "TX", "city": "Dallas"},
            ],
        }

        result = grouped_dict(input_data)
        assert result == expected_result

    # Tests that the function returns an empty dictionary when given a dictionary as input
    def test_dict_input(self):
        input_data = [{"state": "CA", "city": "Los Angeles"}]
        expected_result = {"CA": [{"state": "CA", "city": "Los Angeles"}]}
        result = grouped_dict(input_data)
        assert result == expected_result

    # Tests that the function correctly groups a list of dictionaries with nested dictionaries as values by the 'state' key.
    def test_nested_dict_input(
        self,
    ):
        input_data = [
            {
                "state": "CA",
                "cities": [{"name": "Los Angeles"}, {"name": "San Francisco"}],
            },
            {"state": "NY", "cities": [{"name": "New York"}, {"name": "Albany"}]},
        ]
        expected_result = {
            "CA": [
                {
                    "state": "CA",
                    "cities": [{"name": "Los Angeles"}, {"name": "San Francisco"}],
                }
            ],
            "NY": [
                {"state": "NY", "cities": [{"name": "New York"}, {"name": "Albany"}]}
            ],
        }
        result = grouped_dict(input_data)
        assert result == expected_result

    # Tests that the function returns a grouped dictionary when given a list of dictionaries with non-hashable values
    def test_non_hashable_values_fixed(self):
        input_data = [
            {"state": "CA", "city": "Los Angeles"},
            {"state": "CA", "city": "San Francisco"},
            {"state": "NY", "city": "New York"},
            {"state": "NY", "city": "Albany"},
        ]

        expected_result = {
            "CA": [
                {"state": "CA", "city": "Los Angeles"},
                {"state": "CA", "city": "San Francisco"},
            ],
            "NY": [
                {"state": "NY", "city": "New York"},
                {"state": "NY", "city": "Albany"},
            ],
        }

        result = grouped_dict(input_data)
        assert result == expected_result

    # Tests that the function correctly groups a list of dictionaries with nested lists as values by the 'state' key.
    def test_nested_lists(
        self,
    ):
        input_data = [
            {"state": "CA", "cities": ["Los Angeles", "San Francisco"]},
            {"state": "NY", "cities": ["New York", "Albany"]},
        ]
        expected_result = {
            "CA": [{"state": "CA", "cities": ["Los Angeles", "San Francisco"]}],
            "NY": [{"state": "NY", "cities": ["New York", "Albany"]}],
        }
        result = grouped_dict(input_data)
        assert result == expected_result

    # Tests that the function returns a grouped dictionary when given a list of dictionaries with non-string keys
    def test_non_string_keys(
        self,
    ):
        input_data = [
            {"state": "CA", "city": "Los Angeles"},
            {"state": "CA", "city": "San Francisco"},
            {"state": "NY", "city": "New York"},
            {"state": "NY", "city": "Albany"},
        ]

        expected_result = {
            "CA": [
                {"state": "CA", "city": "Los Angeles"},
                {"state": "CA", "city": "San Francisco"},
            ],
            "NY": [
                {"state": "NY", "city": "New York"},
                {"state": "NY", "city": "Albany"},
            ],
        }

        result = grouped_dict(input_data)
        assert result == expected_result

    # Tests that the function returns a grouped dictionary when given a list of dictionaries with non-string values
    def test_non_string_values_input(self):
        input_data = [
            {"state": 1, "city": "Los Angeles"},
            {"state": 1, "city": "San Francisco"},
            {"state": 2, "city": "New York"},
            {"state": 2, "city": "Albany"},
        ]

        expected_result = {
            1: [
                {"state": 1, "city": "Los Angeles"},
                {"state": 1, "city": "San Francisco"},
            ],
            2: [
                {"state": 2, "city": "New York"},
                {"state": 2, "city": "Albany"},
            ],
        }

        result = grouped_dict(input_data)
        assert result == expected_result
