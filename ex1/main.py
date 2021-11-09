from ex1 import yaml_appender

if __name__ == '__main__':
    yaml_appender = yaml_appender.FileToMemoryYamlAppender('inputs/base.yaml')
    yaml_appender.append_yaml('inputs/config.yaml', 'output.yaml')

