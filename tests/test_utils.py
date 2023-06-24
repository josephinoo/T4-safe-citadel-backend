from src.utils import grouped_dict


class TestGroupedDict:
    # Tests that the function groups a list of dictionaries with unique values for the group_by key
    def test_unique_values(self):
        input_list = [{"a": 1}, {"a": 2}, {"a": 3}]
        group_by = "a"
        expected_output = {1: [{"a": 1}], 2: [{"a": 2}], 3: [{"a": 3}]}
        assert grouped_dict(input_list, group_by) == expected_output

    # Tests that the function returns an empty dictionary when given an empty list
    def test_empty_list(self):
        input_list = []
        group_by = "a"
        expected_output = {}
        assert grouped_dict(input_list, group_by) == expected_output

    # Tests that the function returns a dictionary with a single key-value pair when given a list containing only one dictionary
    def test_single_dict(self):
        input_list = [{"a": 1}]
        group_by = "a"
        expected_output = {1: [{"a": 1}]}
        assert grouped_dict(input_list, group_by) == expected_output
