from ex1.yaml_appender import FileToMemoryYamlAppender

if __name__ == '__main__':
    yaml_appender = FileToMemoryYamlAppender('inputs/base.yaml')
    yaml_appender.append_yaml('inputs/config.yaml', 'output.yaml')

