import yaml
from ex1.merge_utils import merge_dicts


def _yaml_to_dict(yaml_path: str) -> dict:
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


class FileToMemoryYamlAppender:
    def __init__(self, base_yaml_path):
        self.base_yaml_path = base_yaml_path

    def append_yaml(self, config_yaml_path, merged_yaml_path=None):
        """
        :param config_yaml_path: string containing the path to the input yaml configuration
        :param merged_yaml_path: optional string containing the path the output yaml file,
        if not specified will override original base yaml
        """
        base_dict, config_dict = _yaml_to_dict(self.base_yaml_path), _yaml_to_dict(config_yaml_path)
        merged_dict = merge_dicts(config_dict, base_dict)
        merged_path = merged_yaml_path if merged_yaml_path is not None else self.base_yaml_path
        with open(merged_path, 'w') as f:
            yaml.dump(merged_dict, f)
