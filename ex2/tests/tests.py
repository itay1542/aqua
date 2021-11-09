import unittest
import os
import shutil
import functools
from ex2.errors import CircularDependencyError
from ex2.requirements_processing import RequirementsProcessor


def create_mock_files(base_dir, deps, recursive_dep_level=0):
    os.mkdir(base_dir)
    with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
        for dep in deps:
            f.write(F"{dep}\n")
        if recursive_dep_level > 0:
            f.write("\n-r requirements1.txt\n")

    if recursive_dep_level > 0:
        for i in range(1, recursive_dep_level):
            with open(os.path.join(base_dir, F"requirements{i}.txt"), "w") as f:
                for dep in deps:
                    f.write(F"{i}{dep}\n")
                f.write(F"\n-r requirements{i+1}")
        with open(os.path.join(base_dir, F"requirements{recursive_dep_level}.txt"), "w") as f:
            f.writelines([F"{recursive_dep_level}{dep}\n" for dep in deps])


class RequirementsProcessingTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.basedir = ".\\requirements"
        super(RequirementsProcessingTests, self).__init__(*args, **kwargs)

    def tearDown(self):
        shutil.rmtree(self.basedir)

    def test_no_recursion(self):
        create_mock_files(self.basedir, ["numpy>=1.0.0", "pandas<=1.0.0"])
        expected = "numpy>=1.0.0,pandas<=1.0.0"
        actual = RequirementsProcessor(self.basedir).requirements_file_to_string("requirements.txt")
        self.assertEqual(expected, actual)

    def test_recursion(self):
        create_mock_files(self.basedir, ["numpy>=1.0.0", "pandas<=1.0.0"], 1)
        expected = "numpy>=1.0.0,pandas<=1.0.0,1numpy>=1.0.0,1pandas<=1.0.0"
        actual = RequirementsProcessor(self.basedir).requirements_file_to_string("requirements.txt")
        self.assertEqual(expected, actual)

    def test_circular_dep_throws_error(self):
        create_mock_files(self.basedir, ["numpy>=1.0.0", "pandas<=1.0.0"], 1)
        with open(os.path.join(self.basedir, "requirements1.txt"), "w") as f:
            f.write("\n-r requirements.txt")
        to_throw = functools.partial(RequirementsProcessor(self.basedir).requirements_file_to_string, "requirements.txt")
        self.assertRaises(CircularDependencyError, to_throw)


if __name__ == '__main__':
    unittest.main()
