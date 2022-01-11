from typing import Any, List


class OneHotEncoder:
    def __init__(self, discrete_values: List[Any]):
        self.discrete_values = discrete_values

    def one_hot_encode(self, values: List[Any]):
        one_hot_encoded_values: List[Any] = []
        for val in values:
            one_hot_encoded_values += [
                1 if val == value else 0 for value in self.discrete_values
            ]

        return one_hot_encoded_values
