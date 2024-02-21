import re
import os

class Preprocessor:
    def __init__(self):
        self.possibly_sensitive_lines = set()

    def file_in(self, path):
        try:
            with open(path, 'r') as file:
                content = file.read()
                return (True, content)
        except Exception as e:
            return (False, str(e))

    def file_out(self, path, text):
        try:
            with open(path, 'w') as file:
                file.write(text)
                return (True, "successfully wrote file")
        except Exception as e:
            return (False, str(e))

    def remove_html(self, input_string):
        pattern = '<.*?>'
        clean_text = re.sub(pattern, '', input_string)
        pattern = '{.*?}'
        clean_text = re.sub(pattern, '', clean_text)
        pattern = '&.*?;'
        clean_text = re.sub(pattern, '', clean_text)
        return clean_text

    def _lines_with_pattern(self, input_string, pattern):
        lines = [line for line in input_string.split('\n') if re.search(pattern, line)]
        return lines

    def detect_ssn(self, input_string):
        ssn_pattern = r'\b\d{9}\b'
        return self._lines_with_pattern(input_string, ssn_pattern)

    def detect_dates(self, input_string):
        # for dates such as 07/06/2000
        ddmmyyyy = r'\b\d{2}[-/]\d{2}[-/]\d{4}\b'
        # for dates such as 2000/07/06
        yyyymmdd = r'\b\d{4}[-/]\d{2}[-/]\d{2}\b'
        # for dates such as 6/5/30, 7/28/55, or 11/16/98
        m_d_yy = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2}\b'

        combined_pattern = f'({ddmmyyyy})|({yyyymmdd})|({m_d_yy})'
        return self._lines_with_pattern(input_string, combined_pattern)

    def detect_sensitive_info(self, text):
        # this set will store all of the sensitive lines found in the text
        all_sensitive_lines = set()
        
        # detect lines with dates or 9 digit numbers, and add them to the set of sensitive lines 
        lines_with_dates = self.detect_dates(text)
        all_sensitive_lines.update(lines_with_dates)
        lines_with_ssn = self.detect_ssn(text)
        all_sensitive_lines.update(lines_with_ssn)
        
        # return the set of sensitive lines
        return all_sensitive_lines
    
    def process(self, paths, censored_file_extension=".censored.html"):
        # iterate through the path for each file we want to process
        for path in paths:
            # read that file and retrieve the result. The result will be a tuple (success, message)
            success, message = self.file_in(path)
            
            # if the file was not successfully read, emit an error message
            if not success:
                print(f"Failed to read file {path}. Exception: {message}")

            # if the file was successfully read, `message` will contain the file contents. Detect all sensitive lines
            # in the file and store the set in sensitive_lines variable for further use
            sensitive_lines = self.detect_sensitive_info(message)

            # Split the message into lines, filter out sensitive lines, and rejoin
            message_lines = message.split('\n')
            censored_message_lines = [line for line in message_lines if line not in sensitive_lines]
            censored_message = '\n'.join(censored_message_lines)

            # create a path where we will store the censored file
            censored_path = f"{path}{censored_file_extension}"
            
            # Write the censored message to the censored_path
            success, error_message = self.file_out(censored_path, censored_message)
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
  

