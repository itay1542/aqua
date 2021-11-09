import yaml
from ex1.merge_utils import merge_dicts


class FileToMemoryYamlAppender:
    def __init__(self, base_yaml_path):
        self.base_yaml_path = base_yaml_path

    def append_yaml(self, config_yaml_path, merged_yaml_path=None):
        """
        :param config_yaml_path: string containing the path to the input yaml configuration
        :param merged_yaml_path: optional string containing the path the output yaml file,
        if not specified will override original base yaml
        """
        base_dict, config_dict = self._get_dicts(config_yaml_path)
        merged_dict = merge_dicts(config_dict, base_dict)
        merged_path = merged_yaml_path if merged_yaml_path is not None else self.base_yaml_path
        with open(merged_path, 'w') as f:
            yaml.dump(merged_dict, f)

    def _get_dicts(self, config_yaml_path):
        with open(self.base_yaml_path, 'r') as f:
            base_yaml_dict = yaml.safe_load(f)
        with open(config_yaml_path, 'r') as f:
            input_yaml_dict = yaml.safe_load(f)
        return base_yaml_dict, input_yaml_dict
