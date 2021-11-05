from ex2.requirements_processing import RequirementsProcessor

if __name__ == '__main__':
    print(RequirementsProcessor('.\\inputs').requirements_file_to_string('requirements.txt'))

