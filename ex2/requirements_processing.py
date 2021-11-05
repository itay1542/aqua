import re
import os
from ex2.errors import CircularDependencyError, InvalidDependency

REQUIREMENTS_FILE_TOKEN = "requirements"
RECURSIVE_REQUIREMENTS_FLAG = "-r"


class RequirementsProcessor:
    def __init__(self, requirements_dir):
        self.__requirements_dir = requirements_dir
        self.__requirement_regex = r"\w*(==|>=|<=|~=)([0-9]\.+)*[0-9]"

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
                    requirements.append(self.__process_line(line))
        return ','.join(requirements)

    def __process_line(self, line):
        if REQUIREMENTS_FILE_TOKEN in line and RECURSIVE_REQUIREMENTS_FLAG in line:
            deep_requirements_file_path = self.__extract_recursive_dependency_path(line)
            self.__validate_dependency_path(deep_requirements_file_path)
            return self.requirements_file_to_string(deep_requirements_file_path)
        else:
            self._validate_requirement(line)
            return line.strip()

    def __extract_recursive_dependency_path(self, line):
        return re.sub(' +', ' ', line).strip().split(' ')[-1]

    def __validate_dependency_path(self, file):
        if not file.endswith('.txt'):
            raise NameError("requirements file is not a text file")
        if not os.path.isfile(os.path.join(self.__requirements_dir, file)):
            raise FileNotFoundError(F"file {file} does not exist in the requirements directory")

    def _validate_requirement(self, version):
        if not re.compile(self.__requirement_regex).match(version):
            raise InvalidDependency(F"{version} is not a valid dependency")
