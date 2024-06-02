import re
from random import choice

extraction_pattern = re.compile(
    r'heading\s+is([a-zA-Z\s,\-]+?)\s*(?=tool\s+to\s+deploy\s+is|target\s+is|\.|$)|'
    r'tool\s+to\s+deploy\s+is([a-zA-Z\s,\-]+?)\s*(?=heading\s+is|target\s+is|\.|$)|'
    r'target\s+is([a-zA-Z\s,\-]+?)\s*(?=heading\s+is|tool\s+to\s+deploy\s+is|\.|$)',
    re.IGNORECASE
)

def extract_parts(text):
    
    matches = extraction_pattern.finditer(text)
    
    result = {}
    for match in matches:
        if match.group(1):
            result['heading'] = match.group(1).strip(" ,")
        elif match.group(2):
            result['tool'] = match.group(2).strip(" ,")
        elif match.group(3):
            result['target'] = match.group(3).strip(" ,")
    
    return result
    
def convert_numbers(orig):

    # Mapping of words to numbers
    numbers = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'niner': 9, 'nine': 9,
    }
    
    orig_words = orig.split(" ")
    result = ""
    
    # Performs conversion stepwise to catch exceptions.
    for i in orig_words:
        try:
            result += str(numbers[i])
        except KeyError:            
            result += str(choice(numbers.values()))

    return result

def parse_transcript(text):
    """Converts the transcript to the dict form for NLP."""
    
    extraction = extract_parts(text)
    
    # Converts the headings, but skips this step if the heading can't be found.
    try:
        extraction['heading'] = convert_numbers(extraction['heading'])
    except KeyError:
        pass
    
    return extraction

class NLPManager:
    def __init__(self):
        pass

    def qa(self, context: str):
        return parse_transcript(context)
