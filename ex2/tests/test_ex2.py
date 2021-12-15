import pytest
import functools
from ex2.errors import CircularDependencyError, InvalidDependency
from ex2.requirements_processing import RequirementsProcessor
import unittest.mock as mock


def _open_mock_requirements_with_depth(dependencies: list, depth: int, filename: str, *args):
    content = ""
    if "requirements.txt" in filename:
        for dep in dependencies:
            content += F"{dep}\n"
        if depth > 0:
            content += "-r requirements1.txt\n"
    else:
        file_depth_level = int(filename[1:].split('.')[0][-1])
        for dep in dependencies:
            content += F"{file_depth_level}{dep}\n"
        if file_depth_level < depth:
            content += F"requirements{file_depth_level+1}.txt"
    file_object = mock.mock_open(read_data=content).return_value
    file_object.__iter__.return_value = content.splitlines(True)
    return file_object


def _open_mock_with_circular_dep(filename: str, *args):
    content = ""
    _open_mock_requirements_with_depth([], 1, "requirements.txt")
    if "requirements1.txt" in filename:
        content += "-r requirements.txt\n"
    file_object = mock.mock_open(read_data=content).return_value
    file_object.__iter__.return_value = content.splitlines(True)
    return file_object


class TestClass:
    def test_sanity_returns_correct_string_when_not_given_recursive_dependency(self):
        mock_open = mock.mock_open()
        mock_open.side_effect = functools.partial(_open_mock_requirements_with_depth, ["numpy>=1.0.0", "pandas<=1.0.0"], 0)
        with mock.patch('ex2.requirements_processing.open', mock_open):
            expected = "numpy>=1.0.0,pandas<=1.0.0"
            actual = RequirementsProcessor('.\\requirements').requirements_file_to_string("requirements.txt")
            assert expected == actual

    @mock.patch('os.path.isfile', new=lambda x: True)
    def test_includes_deep_requirements_when_given_recursive_dependency(self):
        mock_open = mock.mock_open()
        mock_open.side_effect = functools.partial(_open_mock_requirements_with_depth, ["numpy>=1.0.0", "pandas<=1.0.0"], 1)
        with mock.patch('ex2.requirements_processing.open', mock_open):
            expected = "numpy>=1.0.0,pandas<=1.0.0,1numpy>=1.0.0,1pandas<=1.0.0"
            actual = RequirementsProcessor('.\\requirements').requirements_file_to_string("requirements.txt")
            assert expected == actual

    @mock.patch('os.path.isfile', new=lambda x: True)
    def test_raises_CircularDependencyError_when_given_reference_to_seen_file(self):
        mock_open = mock.mock_open()
        mock_open.side_effect = functools.partial(_open_mock_with_circular_dep, "requirements1.txt")
        with mock.patch('ex2.requirements_processing.open', mock_open):
            with pytest.raises(CircularDependencyError):
                RequirementsProcessor('.\\requirements').requirements_file_to_string(base_file='requirements.txt')

    @mock.patch('os.path.isfile', new=lambda x: True)
    def test_raises_InvalidDependency_when_given_file_without_flag(self):
        mock_open = mock.mock_open(read_data="pandas<=1.0.0\nrequirements.txt")
        with mock.patch('ex2.requirements_processing.open', mock_open):
            with pytest.raises(InvalidDependency):
                RequirementsProcessor('.\\requirements').requirements_file_to_string(base_file='requirements.txt')

    @mock.patch('os.path.isfile', new=lambda x: True)
    def test_raises_InvalidDependency_when_given_file_with_wrong_flag(self):
        mock_open = mock.mock_open(read_data="pandas<=1.0.0\n-really requirements2.txt")
        with mock.patch('ex2.requirements_processing.open', mock_open):
            with pytest.raises(InvalidDependency):
                RequirementsProcessor('.\\requirements').requirements_file_to_string(base_file='requirements.txt')

    @mock.patch('os.path.isfile', new=lambda x: True)
    def test_ignores_one_recursive_dependency_when_given_two_identical_ones(self):
        with mock.patch('ex2.requirements_processing.open',
                        functools.partial(_open_mock_requirements_with_depth, ["numpy>=1.0.0", "pandas<=1.0.0"], 1)):
            expected = "numpy>=1.0.0,pandas<=1.0.0,1numpy>=1.0.0,1pandas<=1.0.0"
            actual = RequirementsProcessor('.\\requirements').requirements_file_to_string("requirements.txt")
            assert expected == actual
