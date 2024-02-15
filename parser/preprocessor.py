import re
import os

class Preprocessor:
    def __init__(self):
        self.possibly_sensitive_lines = set()

    def file_in(self, paths):
        files = []
        for path in paths:
            try:
                with open(path, 'r') as file:
                    content = file.read()
                    files.append((True, content))

            except Exception as e:
                print(f"Error occured in file_in: {e}\n")
                files.append((False, str(e)))
        return files

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
        ddmmyyyy = r'\b\d{2}[-/]\d{2}[-/]\d{4}\b'
        yyyymmdd = r'\b\d{4}[-/]\d{2}[-/]\d{2}\b'
        combined_pattern = f'({ddmmyyyy})|({yyyymmdd})'
        return self._lines_with_pattern(input_string, combined_pattern)

    def process(self, paths):
        file_strings = self.file_in(paths)
        all_sensitive_lines = set()

        # Loop through the lines in the files
        for success, file_string in file_strings:
            if not success:
                print(f"Error occured in process: {file_string}\n")
                continue
        
            p_text = file_string # Can be cleaned using p_text = self.remove_html(file_string) instead (written below)
            # p_text = self.remove_html(file_string)
            lines_with_dates = self.detect_dates(p_text)
            all_sensitive_lines.update(lines_with_dates)
            lines_with_ssn = self.detect_ssn(p_text)
            all_sensitive_lines.update(lines_with_ssn)
        
        self.possibly_sensitive_lines = all_sensitive_lines

        return all_sensitive_lines # Return all lines with sensitive information


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
  

