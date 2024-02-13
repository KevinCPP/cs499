import re

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

    def process(self, path):
        success, file_string = self.file_in(path)

        if not success:
            return (False, file_string)
        
        p_text = file_string
        lines_with_dates = self.detect_dates(p_text)
        self.possibly_sensitive_lines.update(lines_with_dates)
        lines_with_ssn = self.detect_ssn(p_text)
        self.possibly_sensitive_lines.update(lines_with_ssn)

        return (True, self.possibly_sensitive_lines) 


if __name__ == "__main__":
    p = Preprocessor()
    file = "messages/test.html"
    print("========= Lines with sensitive info detected =========")
    success, lines = p.process(file, "test")

