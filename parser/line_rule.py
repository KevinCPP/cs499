import re

def lr_dob_and_ssn(input_text):
    # pattern for 9 digit numbers
    ssn_pattern = r'\b\d{9}\b'
    # for dates such as 07/06/2000
    ddmmyyyy = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b'
    # for dates such as 2000/07/06
    yyyymmdd = r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b'
    # combined pattern for detecting dates
    date_pattern = f'({ddmmyyyy})|({yyyymmdd})'

    indices = []
    for index, line in enumerate(input_text.splitlines()):
        if re.search(ssn_pattern, line) and re.search(date_pattern, line):
            indices.append((index, index))

    return indices


def lr_two_blank_lines(input_text):
    indices = []
    start_index = -1
    for index, line in enumerate(input_text.splitlines()):
        if not line.strip():
            if start_index == -1:
                start_index = index

        else:
            if start_index != -1 and index-start_index >= 2:
                indices.append((start_index, index))
                start_index = -1

    return indices

