import os
from ex2.errors import CircularDependencyError
from ex2.validations import validate_dependency_path, validate_requirement
from ex2.utils import extract_recursive_dependency_path

REQUIREMENTS_FILE_TOKEN = "requirements"
RECURSIVE_REQUIREMENTS_FLAG = "-r"


class RequirementsProcessor:
    def     __init__(self, requirements_dir):
        self.__requirements_dir = requirements_dir
        # to prevent circular dependency
        self.__seen_files = []

    def requirements_file_to_string(self, base_file):
        requirements = []
        file_path = os.path.join(self.__requirements_dir, base_file)
        if file_path in self.__seen_files:
            raise CircularDependencyError(F"circular dependency detected for file {file_path}")
        self.__seen_files.append(file_path)
        with open(file_path, 'r') as f:
            while line := f.readline():
                if line.strip() != '':
                    requirements.append(self.__get_requirement_string_from_line(line))
        return ','.join(requirements)

    def __get_requirement_string_from_line(self, line):
        if REQUIREMENTS_FILE_TOKEN in line and RECURSIVE_REQUIREMENTS_FLAG in line:
            deep_requirements_file_path = extract_recursive_dependency_path(line)
            validate_dependency_path(deep_requirements_file_path, self.__requirements_dir)
            return self.requirements_file_to_string(deep_requirements_file_path)
        else:
            validate_requirement(line)
            return line.strip()
