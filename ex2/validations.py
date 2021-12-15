import re
import os

from ex2.consts import REQUIREMENT_FILE_FORMAT_SUFFIX, REQUIREMENT_REGEX
from ex2.errors import InvalidDependency


def validate_dependency_path(file, dir):
    if not file.endswith(REQUIREMENT_FILE_FORMAT_SUFFIX):
        raise NameError("requirements file is not a text file")
    if not os.path.isfile(os.path.join(dir, file)):
        raise FileNotFoundError(F"file {file} does not exist in the requirements directory")


def validate_requirement_format(version):
    if not re.compile(REQUIREMENT_REGEX).match(version):
        raise InvalidDependency(F"{version} is not a valid dependency")