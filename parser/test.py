import re

def find_substrings_by_regex(text, start_regex, end_regex):
    """
    Finds all non-overlapping substrings in a text that start and end with given regex patterns.
    
    Parameters:
        text (str): The text to search within.
        start_regex (str): The regex pattern that the substrings should start with.
        end_regex (str): The regex pattern that the substrings should end with.
    
    Returns:
        list: A list of substrings that match the criteria.
    """
    # Combine the start and end regex patterns into a single pattern
    pattern = f"({start_regex}).*?({end_regex})"
    
    # Find all non-overlapping matches of the pattern in the text
    matches = re.finditer(pattern, text)
    
    # Extract the matched substrings from the text
    substrings = [match.group(0) for match in matches]
    
    return substrings

# Example usage
text = "Here is a start example end, and here is another start sample text end."
start_regex = "start"
end_regex = "end"
substrings = find_substrings_by_regex(text, start_regex, end_regex)
print("Found substrings:", substrings)

