import re
import os

from parser.file_io import file_in
from parser.file_io import file_out
from parser.parser import remove_html

class Preprocessor:
    def __init__(self):
        # pattern for detecting 9 digit numbers (social security numbers or medical record numbers)
        self.ssn_pattern = r'\b\d{9}\b'
        self.parser = Parser()

        # for dates such as 07/06/2000
        ddmmyyyy = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'
        # for dates such as 2000/07/06
        yyyymmdd = r'\b\d{2,4}[-/]\d{1,2}[-/]\d{1,2}\b'
        # combined pattern for detecting dates
        self.date_pattern = f'({ddmmyyyy})|({yyyymmdd})'

        # detect phone numbers such as (555) 555-5555, 555-555-5555, and so  on...
        formatted_phone_number = r'(?:\(\d{3}\)\s?|\b\d{3}[-\s])\d{3}[-]?\d{4}\b'
        # detect basic 10-digit phone numbers such as 5555555555
        basic_ten_digit_number = r'\b\d{10}\b'
        # combined pattern for detecting phone numbers
        self.phone_number_pattern = f"({formatted_phone_number})|({basic_ten_digit_number})" 
        
#    def remove_html(self, input_string, replace_with=' '):
#        pattern = '<.*?>'
#        clean_text = re.sub(pattern, replace_with, input_string)
#        pattern = '{.*?}'
#        clean_text = re.sub(pattern, replace_with, clean_text)
#        pattern = '&.*?;'
#        clean_text = re.sub(pattern, replace_with, clean_text)
#        return clean_text
    
    def censor_sensitive_information(self, text):
        # detect if we possibly failed to censor a name:
        name_censored = False

        # first, we will substitute all 9 digit numbers (MRNs or SSNs) with 666666666
        censored_text = re.sub(self.ssn_pattern, '666666666', text)
        # then we will censor all dates that could possibly be a DOB with 2000/01/01
        censored_text = re.sub(self.date_pattern, '2000/01/01', censored_text)
        # finally, we will censor all phone numbers by replacing them with 555-555-5555
        censored_text = re.sub(self.phone_number_pattern, '555-555-5555', censored_text)
        
        # split the censored text into individual lines (we'll use this to attempt to censor names)
        censored_text_lines = censored_text.split('\n')
        # iterate through each line
        for line in censored_text_lines:
            # if the line contains both a 9 digit SSN/MRN pattern and a date, it's likely a line that contains the patient's
            # information, such as "FirstName MI. LastName SSN/MRN DOB"
            if re.search(self.ssn_pattern, line) and re.search(self.date_pattern, line):
                # tokenize this line so that we can extract what could possibly be a date. This will first require scrubbing
                # it of HTML to avoid removing HTML elements from the rest of the document. We only want to remove names if we're
                # absolutely sure that it's a name, to avoid removing any necessary information.
                line_no_html = self.parser.remove_html(line)
                # split at any whitespace. This works because remove_html will replace html tags with a whitespace character by default.
                tokenized_line_no_html = line_no_html.split()
                
                # remove the tokens matching the date since we want to narrow it down to the names only
                filtered_tokens = [s for s in tokenized_line_no_html if not re.search(self.date_pattern, s)]
                # remove the tokens matching the ssn/mrn since we want to narrow it down to the names only
                filtered_tokens = [s for s in filtered_tokens if not re.search(self.ssn_pattern, s)]
                # since a middle initial could be one character (e.g. "F"), we don't want to remove a single character from the whole document, so just ignore it
                filtered_tokens = [s for s in filtered_tokens if (len(s) > 1)]

                # if there are 2 or 3 tokens remaining (e.g. ["FirstName", "LastName"] or ["First", "Middle", "Last"]) remove them
                if len(filtered_tokens) == 2 or len(filtered_tokens) == 3:
                    # print what we are removing (debug feature)
                    print(f"Removing the tokens: {filtered_tokens}")
                    # remove the tokens from the censored text as a whole 
                    for token in filtered_tokens:
                        censored_text = censored_text.replace(token, "__NAME__")
                    
                    # set name_censor_failed to False
                    name_censored = True
        
        # finally, return whether or not we censored any names, and the final censored text
        return (name_censored, censored_text)
                

    def process(self, paths, censored_file_extension=".censored.html"):
        # iterate through the path for each file we want to process
        for path in paths:
            # read that file and retrieve the result. The result will be a tuple (success, message)
            success, message = file_in(path)
            
            # if the file was not successfully read, emit an error message
            if not success:
                print(f"Failed to read file {path}. Exception: {message}")
                return

            name_censored, censored_message = self.censor_sensitive_information(message)
            
            # create a path where we will store the censored file
            censored_path = f"{path}{censored_file_extension}"

            if not name_censored:
                print(f"WARN: Name possibly not censored for {path}")
                censored_path = f"{censored_path}.WARN"
            
            # Write the censored message to the censored_path
            success, error_message = file_out(censored_path, censored_message)
            if not success:
                print(f"Failed to write censored file {censored_path}. Exception: {error_message}")

if __name__ == "__main__":
    p = Preprocessor()
    path = "messages"

    # Choose the entire messages directory or certain messages
    files  = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    #files = ["messages/test.html", "messages/20210816-Call 8_15-1313.html", "messages/20210815-Re_Call 8_14-1316.html", "messages\20210814-Call Email 8_13-1320.html"]
    
    print("\n=================== Lines with sensitive info detected ===================\n")
    lines = p.process(files)
    for line in lines:
        print(line, "\n")
    print("============================================================================\n")
  

