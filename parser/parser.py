import re
import os

from parser.file_io import *
from parser.line_rule import *

class Parser:
    def __init__(self):
        # pattern for 9 digit numbers
        self.ssn_pattern = r'\b\d{9}\b'
        # for dates such as 07/06/2000
        ddmmyyyy = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'
        # for dates such as 2000/07/06
        yyyymmdd = r'\b\d{2,4}[-/]\d{1,2}[-/]\d{1,2}\b'
        # combined pattern for detecting dates
        self.date_pattern = f'({ddmmyyyy})|({yyyymmdd})'

    # strips html from the input string and returns the cleaned text
    def remove_html(self, input_string, replace_with=' '):
        pattern = '<.*?>'
        clean_text = re.sub(pattern, replace_with, input_string)
        pattern = '{.*?}'
        clean_text = re.sub(pattern, replace_with, clean_text)
        pattern = '&.*?;'
        clean_text = re.sub(pattern, replace_with, clean_text)
        return clean_text

    def _group_substr(self, input_string, start_matches, end_matches) -> list:
        # build up a list/stack containing all of the substrings
        substrings = []
        # no end position has been encountered yet, initialize to -1
        end_pos_last = -1

        # iterate through all start matches (start, end) indices
        for start_pos, start_end in start_matches:
            # if the start of this start match is before the end of the last
            # ending position, ignore. This will not be counted for the first
            # starting pos since end_pos_last is initialized to -1
            if start_pos < end_pos_last:
                continue
            
            # iterate through end positions, finding the first one that is after this start_pos
            for end_pos, end_end in end_matches:
                if end_pos >= start_end:
                    # add the substring to the list of solutions
                    substrings.append(input_string[start_pos:end_end])
                    # update last ending flag that was found
                    end_pos_last = end_end
                    break
        
        # return all of the substrings
        return substrings
    
    # return all substrings which start with start_regex and end with end_regex (not inclusive)
    def get_excerpt(self, input_string, start_regex, end_regex) -> list:
        # Find all matches for start and end regex
        start_matches = [(match.start(), match.end()) for match in re.finditer(start_regex, input_string)]
        end_matches = [(match.start(), match.end()) for match in re.finditer(end_regex, input_string)]

        # return the matches
        return self._group_substr(input_string, start_matches, end_matches)
    
    # return all substrings which start with the start_line_rule and end with the end_line_rule
    def get_section(self, input_string, start_line_rule, end_line_rule) -> list:
        # Find all matches for start/end line rules
        start_matches = start_line_rule(input_string)
        end_matches = end_line_rule(input_string)
        
        # build up a list/stack containing all of the substrings
        substrings = []
        # no end position has been encountered yet, initialize to -1
        end_pos_last = -1

        # iterate through all start matches (start, end) indices
        for start_pos, start_end in start_matches:
            # if the start of this start match is before the end of the last
            # ending position, ignore. This will not be counted for the first
            # starting pos since end_pos_last is initialized to -1
            if start_pos < end_pos_last:
                continue
            
            # iterate through end positions, finding the first one that is after this start_pos
            for end_pos, end_end in end_matches:
                if end_pos >= start_end:
                    lines = input_string.splitlines()
                    # add the substring to the list of solutions
                    substrings.append("\n".join(lines[start_pos:end_end]))
                    # update last ending flag that was found
                    end_pos_last = end_end
                    break
        
        # return all of the substrings
        return substrings

    def get_patients(self, input_string) -> list:
        return self.get_section(self.remove_html(input_string), lr_dob_and_ssn, lr_two_blank_lines)

if __name__ == "__main__":
    success, text = file_in("test.html")
    if not success:
        print("failed to read email")
        exit(0)

    parser = Parser()
    patients = parser.get_patients(text)
    print(patients)
    print("-"*20)
    for p in patients:
        print(p)
