import re


def extract_recursive_dependency_path(line):
    return re.sub(' +', ' ', line).strip().split(' ')[-1]
