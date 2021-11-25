import unittest
import functools
from ex2.errors import CircularDependencyError
from ex2.requirements_processing import RequirementsProcessor
import unittest.mock as mock


def _open_deep(dependencies: list, depth: int, filename: str, *args):
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


def _open_circular_dep(filename: str, *args):
    content = ""
    _open_deep([], 1, "requirements.txt")
    if "requirements1.txt" in filename:
        content += "-r requirements.txt\n"
    file_object = mock.mock_open(read_data=content).return_value
    file_object.__iter__.return_value = content.splitlines(True)
    return file_object


class RequirementsProcessingTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.basedir = ".\\requirements"
        super(RequirementsProcessingTests, self).__init__(*args, **kwargs)

    @mock.patch('ex2.requirements_processing.open', new=functools.partial(_open_deep, ["numpy>=1.0.0", "pandas<=1.0.0"], 0))
    def test_no_recursion(self):
        expected = "numpy>=1.0.0,pandas<=1.0.0"
        actual = RequirementsProcessor(self.basedir).requirements_file_to_string("requirements.txt")
        self.assertEqual(expected, actual)

    @mock.patch('ex2.requirements_processing.open', new=functools.partial(_open_deep, ["numpy>=1.0.0", "pandas<=1.0.0"], 1))
    @mock.patch('os.path.isfile', new=lambda x: True)
    def test_recursion(self):
        expected = "numpy>=1.0.0,pandas<=1.0.0,1numpy>=1.0.0,1pandas<=1.0.0"
        actual = RequirementsProcessor(self.basedir).requirements_file_to_string("requirements.txt")
        self.assertEqual(expected, actual)

    @mock.patch('ex2.requirements_processing.open', new=functools.partial(_open_circular_dep, "requirements1.txt"))
    @mock.patch('os.path.isfile', new=lambda x: True)
    def test_circular_dep_throws_error(self):
        to_throw = RequirementsProcessor(self.basedir).requirements_file_to_string
        self.assertRaises(CircularDependencyError, to_throw, base_file='requirements.txt')


if __name__ == '__main__':
    unittest.main()
