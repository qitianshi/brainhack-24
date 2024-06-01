import re
import cmudict
from random import choice
from difflib import SequenceMatcher
from transformers import BartForConditionalGeneration, BartTokenizer, AutoTokenizer
from os import path

# Initialized only if needed.
phonetics = None
tokenizer_name = path.join(path.dirname(path.abspath(__file__)), "tokenizer")
model_name = path.join(path.dirname(path.abspath(__file__)), "correction_model")
tokenizer = None
model = None

extraction_pattern = re.compile(
    r'heading\s+is\s+([a-zA-Z\s,\-]+?)\s*(?=tool\s+to\s+deploy\s+is|target\s+is|\.|$)|'
    r'tool\s+to\s+deploy\s+is\s+([a-zA-Z\s,\-]+?)\s*(?=heading\s+is|target\s+is|\.|$)|'
    r'target\s+is\s+([a-zA-Z\s,\-]+?)\s*(?=heading\s+is|tool\s+to\s+deploy\s+is|\.|$)',
    re.IGNORECASE
)

# Cached for eFfiCiEnCy ( ͡° ͜ʖ ͡° )
number_phonetics = {
    'Z IH1 R OW0': 'zero', 
    'Z IY1 R OW0': 'zero', 
    'W AH1 N': 'one', 
    'T UW1': 'two', 
    'TH R IY1': 'three', 
    'F AO1 R': 'four', 
    'F AY1 V': 'five', 
    'S IH1 K S': 'six', 
    'S EH1 V AH0 N': 'seven', 
    'EY1 T': 'eight', 
    'N AY1 N ER0': 'niner'
}

dual_number_phonetics = {
    'Z IH1 R OW0': 'zero', 
    'Z IY1 R OW0': 'zero', 
    'W AH1 N': 'one', 
    'T UW1': 'two', 
    'TH R IY1': 'three', 
    'F AO1 R': 'four', 
    'F AY1 V': 'five', 
    'S IH1 K S': 'six', 
    'S EH1 V AH0 N': 'seven', 
    'EY1 T': 'eight', 
    'N AY1 N ER0': 'niner',
    'Z IH1 R OW0 Z IH1 R OW0': 'zero zero', 'Z IH1 R OW0 Z IY1 R OW0': 'zero zero', 'Z IY1 R OW0 Z IH1 R OW0': 'zero zero', 'Z IY1 R OW0 Z IY1 R OW0': 'zero zero', 'Z IH1 R OW0 W AH1 N': 'zero one', 'Z IY1 R OW0 W AH1 N': 'zero one', 'Z IH1 R OW0 T UW1': 'zero two', 'Z IY1 R OW0 T UW1': 'zero two', 'Z IH1 R OW0 TH R IY1': 'zero three', 'Z IY1 R OW0 TH R IY1': 'zero three', 'Z IH1 R OW0 F AO1 R': 'zero four', 'Z IY1 R OW0 F AO1 R': 'zero four', 'Z IH1 R OW0 F AY1 V': 'zero five', 'Z IY1 R OW0 F AY1 V': 'zero five', 'Z IH1 R OW0 S IH1 K S': 'zero six', 'Z IY1 R OW0 S IH1 K S': 'zero six', 'Z IH1 R OW0 S EH1 V AH0 N': 'zero seven', 'Z IY1 R OW0 S EH1 V AH0 N': 'zero seven', 'Z IH1 R OW0 EY1 T': 'zero eight', 'Z IY1 R OW0 EY1 T': 'zero eight', 'Z IH1 R OW0 N AY1 N ER0': 'zero niner', 'Z IY1 R OW0 N AY1 N ER0': 'zero niner', 
    'W AH1 N Z IH1 R OW0': 'one zero', 'W AH1 N Z IY1 R OW0': 'one zero', 'W AH1 N W AH1 N': 'one one', 'W AH1 N T UW1': 'one two', 'W AH1 N TH R IY1': 'one three', 'W AH1 N F AO1 R': 'one four', 'W AH1 N F AY1 V': 'one five', 'W AH1 N S IH1 K S': 'one six', 'W AH1 N S EH1 V AH0 N': 'one seven', 'W AH1 N EY1 T': 'one eight', 'W AH1 N N AY1 N ER0': 'one niner', 
    'T UW1 Z IH1 R OW0': 'two zero', 'T UW1 Z IY1 R OW0': 'two zero', 'T UW1 W AH1 N': 'two one', 'T UW1 T UW1': 'two two', 'T UW1 TH R IY1': 'two three', 'T UW1 F AO1 R': 'two four', 'T UW1 F AY1 V': 'two five', 'T UW1 S IH1 K S': 'two six', 'T UW1 S EH1 V AH0 N': 'two seven', 'T UW1 EY1 T': 'two eight', 'T UW1 N AY1 N ER0': 'two niner', 
    'TH R IY1 Z IH1 R OW0': 'three zero', 'TH R IY1 Z IY1 R OW0': 'three zero', 'TH R IY1 W AH1 N': 'three one', 'TH R IY1 T UW1': 'three two', 'TH R IY1 TH R IY1': 'three three', 'TH R IY1 F AO1 R': 'three four', 'TH R IY1 F AY1 V': 'three five', 'TH R IY1 S IH1 K S': 'three six', 'TH R IY1 S EH1 V AH0 N': 'three seven', 'TH R IY1 EY1 T': 'three eight', 'TH R IY1 N AY1 N ER0': 'three niner', 
    'F AO1 R Z IH1 R OW0': 'four zero', 'F AO1 R Z IY1 R OW0': 'four zero', 'F AO1 R W AH1 N': 'four one', 'F AO1 R T UW1': 'four two', 'F AO1 R TH R IY1': 'four three', 'F AO1 R F AO1 R': 'four four', 'F AO1 R F AY1 V': 'four five', 'F AO1 R S IH1 K S': 'four six', 'F AO1 R S EH1 V AH0 N': 'four seven', 'F AO1 R EY1 T': 'four eight', 'F AO1 R N AY1 N ER0': 'four niner', 
    'F AY1 V Z IH1 R OW0': 'five zero', 'F AY1 V Z IY1 R OW0': 'five zero', 'F AY1 V W AH1 N': 'five one', 'F AY1 V T UW1': 'five two', 'F AY1 V TH R IY1': 'five three', 'F AY1 V F AO1 R': 'five four', 'F AY1 V F AY1 V': 'five five', 'F AY1 V S IH1 K S': 'five six', 'F AY1 V S EH1 V AH0 N': 'five seven', 'F AY1 V EY1 T': 'five eight', 'F AY1 V N AY1 N ER0': 'five niner', 
    'S IH1 K S Z IH1 R OW0': 'six zero', 'S IH1 K S Z IY1 R OW0': 'six zero', 'S IH1 K S W AH1 N': 'six one', 'S IH1 K S T UW1': 'six two', 'S IH1 K S TH R IY1': 'six three', 'S IH1 K S F AO1 R': 'six four', 'S IH1 K S F AY1 V': 'six five', 'S IH1 K S S IH1 K S': 'six six', 'S IH1 K S S EH1 V AH0 N': 'six seven', 'S IH1 K S EY1 T': 'six eight', 'S IH1 K S N AY1 N ER0': 'six niner', 
    'S EH1 V AH0 N Z IH1 R OW0': 'seven zero', 'S EH1 V AH0 N Z IY1 R OW0': 'seven zero', 'S EH1 V AH0 N W AH1 N': 'seven one', 'S EH1 V AH0 N T UW1': 'seven two', 'S EH1 V AH0 N TH R IY1': 'seven three', 'S EH1 V AH0 N F AO1 R': 'seven four', 'S EH1 V AH0 N F AY1 V': 'seven five', 'S EH1 V AH0 N S IH1 K S': 'seven six', 'S EH1 V AH0 N S EH1 V AH0 N': 'seven seven', 'S EH1 V AH0 N EY1 T': 'seven eight', 'S EH1 V AH0 N N AY1 N ER0': 'seven niner', 
    'EY1 T Z IH1 R OW0': 'eight zero', 'EY1 T Z IY1 R OW0': 'eight zero', 'EY1 T W AH1 N': 'eight one', 'EY1 T T UW1': 'eight two', 'EY1 T TH R IY1': 'eight three', 'EY1 T F AO1 R': 'eight four', 'EY1 T F AY1 V': 'eight five', 'EY1 T S IH1 K S': 'eight six', 'EY1 T S EH1 V AH0 N': 'eight seven', 'EY1 T EY1 T': 'eight eight', 'EY1 T N AY1 N ER0': 'eight niner', 
    'N AY1 N ER0 Z IH1 R OW0': 'niner zero', 'N AY1 N ER0 Z IY1 R OW0': 'niner zero', 'N AY1 N ER0 W AH1 N': 'niner one', 'N AY1 N ER0 T UW1': 'niner two', 'N AY1 N ER0 TH R IY1': 'niner three', 'N AY1 N ER0 F AO1 R': 'niner four', 'N AY1 N ER0 F AY1 V': 'niner five', 'N AY1 N ER0 S IH1 K S': 'niner six', 'N AY1 N ER0 S EH1 V AH0 N': 'niner seven', 'N AY1 N ER0 EY1 T': 'niner eight', 'N AY1 N ER0 N AY1 N ER0': 'niner niner'
}

def extract(text):
    
    matches = extraction_pattern.finditer(text)
    
    result = {}
    for match in matches:
        if match.group(1):
            result['heading'] = {
                'value': match.group(1).strip(" ,"),
                'start': match.start(1),
                'end': match.end(1)
            }
        elif match.group(2):
            result['tool'] = {
                'value': match.group(2).strip(" ,"),
                'start': match.start(2),
                'end': match.end(2)
            }
        elif match.group(3):
            result['target'] = {
                'value': match.group(3).strip(" ,"),
                'start': match.start(3),
                'end': match.end(3)
            }
    
    return result
    
def extract_parts(extraction):
    
    result = {}
    
    for key, val in extraction.items():
        result[key] = val['value']
    
    return result

def validate_extraction(extraction):
    return all([i in extraction.keys() for i in ['heading', 'tool', 'target']])

def is_vowel(phoneme):
    # Define the sets of vowel and consonant phonemes based on the CMU Pronouncing Dictionary
    # Instead of using the vowel phonemes in the dictionary, 
    vowels = set(['A', 'E', 'I', 'O', 'U', 'Y'])
    return phoneme.rstrip('012') in vowels

def weighted_levenshtein_dist(a, b, consonant_sub_cost=0.5):
    """Compute the weighted Levenshtein distance between two phonetic sequences, with more weight on vowels."""
    
    n, m = len(a), len(b)
    
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row
    
    for i in range(1, m + 1):
        
        previous_row, current_row = current_row, [i] + [0] * n
        
        for j in range(1, n + 1):

            if a[j - 1] == b[i - 1]:
                substitution_cost = 0
            elif is_vowel(a[j - 1]) or is_vowel(b[i - 1]):
                substitution_cost = 1
            else:
                substitution_cost = consonant_sub_cost
                
            current_row[j] = min(previous_row[j] + 1,
                                 current_row[j - 1] + 1,
                                 previous_row[j - 1] + substitution_cost)
    
    return current_row[n]

def norm_weighted_levenshtein_dist(a, b, consonant_sub_cost=0.5):
    """Compute the normalized weighted Levenshtein distance between two phonetic sequences."""
    if not a or not b:
        return 1.0  # If one is empty, max distance
    else:
        return weighted_levenshtein_dist(a, b, consonant_sub_cost) / max(len(a), len(b))

def correct_number(orig, include_duals=False):
    
    global phonetics
    
    if not phonetics:
        phonetics = cmudict.dict()
    
    orig_phonetics_list = phonetics.get(orig)
    
    if orig_phonetics_list:
        
        closest_dist = 1.0
        closest_words = []
        orig_phonetics_list = [' '.join(i) for i in orig_phonetics_list]
        
        # Find closest pronunciation match
        for orig_phonetics in orig_phonetics_list:
            for known_phonetics, known_word in (dual_number_phonetics if include_duals else number_phonetics).items():
                
                dist = norm_weighted_levenshtein_dist(orig_phonetics, known_phonetics)
                
                if dist == closest_dist:
                    # print("=", dist, known_word, known_phonetics, orig_phonetics, sep="\t")
                    closest_words.append(known_word)
                elif dist < closest_dist:
                    # print("<", dist, known_word, known_phonetics, orig_phonetics, sep="\t")
                    closest_dist = dist
                    closest_words.clear()
                    closest_words.append(known_word)
                    
    if not orig_phonetics_list or not closest_words:
        return [choice(list(set(number_phonetics.values())))]    # yolo time
    else:
        return choice(closest_words).split()
    
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
            result += ''.join([str(numbers[j]) for j in correct_number(i, len(orig_words) < 3)])

    return result

def model_correct(orig):
    
    global tokenizer_name, model_name, tokenizer, model
    
    # Load the model if not yet initialized
    if not (tokenizer and model):
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)
        if torch.cuda.is_available():
            model.to('cuda')

    # Tokenize input
    inputs = tokenizer(orig, return_tensors="pt")

    # Generate output
    outputs = model.generate(inputs["input_ids"], max_length=100)

    # Decode output
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
    
def correct_transcript(text):
    """Performs error correction on the transcript but leaves the heading intact."""
    
    # Runs the model, gets the diff
    model_output = model_correct(text)
    diff = SequenceMatcher(None, text, model_output).get_opcodes()
    extraction = extract(model_output)
    
    if 'heading' in extraction.keys():
    
        heading_changes = []
        for i in diff:
            if i[0] != "equal" and any(x in range(extraction['heading']['start'], extraction['heading']['end']) for x in [i[3], i[4]]):
                heading_changes.append(list(i))

        for n, i in enumerate(heading_changes):
            model_output = model_output[:i[3]] + text[i[1]:i[2]] + model_output[i[4]:]
            for j in heading_changes[n+1:]:
                delta = (i[4] - i[3]) - (i[2] - i[1])
                j[3] -= delta
                j[4] -= delta
    
    return model_output

def parse_transcript(text):
    """Converts the transcript to the dict form for NLP."""
    
    extraction = extract_parts(extract(text))
    
    if not validate_extraction(extraction):
        extraction = extract_parts(extract(correct_transcript(text)))
    
    # Converts the headings, but skips this step if the heading can't be found.
    try:
        extraction['heading'] = convert_numbers(extraction['heading'])
    except KeyError:
        pass
    
    return extraction

def reconstruct_transcript(extraction):
    
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "niner"]
    
    result = ""
    for key, val in extraction.items():
        
        result += key + (" to deploy is " if key == "tool" else " is ")
        
        if key == "heading":
            result +=  ' '.join([numbers[int(i)] for i in val])
        else:
            result += val
            
        result += ", "
        
    result = result[0].upper() + result[1:-2] + "."
    
    return result
    