import os

def file_in(path):
    try:
        with open(path, 'r') as file:
            content = file.read()
            return (True, content)
    except Exception as e:
        return (False, str(e))

def file_out(path, text):
    try:
        with open(path, 'w') as file:
            file.write(text)
            return (True, "successfully wrote file")
    except Exception as e:
        return (False, str(e))
