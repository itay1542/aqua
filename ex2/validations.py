import re
import os
from ex2.errors import InvalidDependency

REQUIREMENT_REGEX = r"\w*(==|>=|<=|~=)([0-9]\.+)*[0-9]"
REQUIREMENT_FILE_FORMAT_SUFFIX = ".txt"


def validate_dependency_path(file, dir):
    if not file.endswith(REQUIREMENT_FILE_FORMAT_SUFFIX):
        raise NameError("requirements file is not a text file")
    if not os.path.isfile(os.path.join(dir, file)):
        raise FileNotFoundError(F"file {file} does not exist in the requirements directory")


def validate_requirement(version):
    if not re.compile(REQUIREMENT_REGEX).match(version):
        raise InvalidDependency(F"{version} is not a valid dependency")