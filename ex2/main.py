from ex2.requirements_processing import RequirementsProcessor

if __name__ == '__main__':
    req_processor = RequirementsProcessor('.\\inputs')
    print(req_processor.requirements_file_to_string('requirements.txt'))

