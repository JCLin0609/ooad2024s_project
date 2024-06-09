import json


class FuzzConfig:
    def __init__(self, is_input_by_file: bool = False):
        self.is_input_by_file = is_input_by_file

    @classmethod
    def from_json(cls, json_str: str):
        config_dict = json.loads(json_str)
        return cls(is_input_by_file=config_dict['isInputByFile'])
