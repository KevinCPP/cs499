import re

if __name__ == "__main__":
    # Updated pattern to match phone number formats more strictly
    # Enforces correct spacing/delimiters and avoids matching date-like numbers
#    pattern = r'\b(?:\(\d{3}\)\s?-?\d{3}-?\d{4}|\b\d{3}[-\s]?\d{3}[-]?\d{4}|\b\d{10}\b)'
    phone_number = r'(?:\(\d{3}\)\s?|\b\d{3}[-\s])\d{3}[-]?\d{4}\b'
    ten_digit = r'\b\d{10}\b'
    pattern = f"({phone_number})|({ten_digit})" 

    # Example strings to test the updated pattern
    test_strings = [
        "(555) 555-5555",
        "555-555-5555",
        "5555555555",
        "(555) 5555555",
        "(555)555-5555",
        "(555)5555555",
        "Jane Doe 1/1/1901 111111111",  # This should not match
        "5 555555555"  # This should not match
    ]

    # Checking each string against the updated pattern
    for string in test_strings:
        if re.search(pattern, string):
            print(f"Match found: {string}")
        else:
            print(f"No match: {string}")
