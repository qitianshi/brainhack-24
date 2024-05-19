from typing import Dict
from transformers import RobertaTokenizer, RobertaForQuestionAnswering
import torch

class NLPManager:
    
    def __init__(self):
        
        # Load the tokenizer and model
        self.tokenizer = RobertaTokenizer.from_pretrained('deepset/roberta-base-squad2')
        self.model = RobertaForQuestionAnswering.from_pretrained('deepset/roberta-base-squad2')

        # Specify the device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    @staticmethod
    def convert_numbers(orig: str) -> str:
        
        # Mapping of words to numbers
        numbers = {
            'one': 1, 'five': 5, 'zero': 0, 'two': 2, 'six': 6,
            'niner': 9, 'seven': 7, 'three': 3, 'four': 4, 'eight': 8
        }
        
        result = "".join(str(numbers[word]) for word in orig.split(" "))
        
        return result

    def get_answer(self, question: str, context: str) -> str:
        
        inputs = self.tokenizer.encode_plus(question, context, return_tensors='pt').to(self.device)
        input_ids = inputs['input_ids'].tolist()[0]
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            answer_start_scores = outputs.start_logits
            answer_end_scores = outputs.end_logits

        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1

        return self.tokenizer.convert_tokens_to_string(self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    def qa(self, context: str) -> Dict[str, str]:
        
        heading = self.convert_numbers(self.get_answer("What is the heading?", context).strip())
        target = self.get_answer("What is the target?", context).strip()
        tool = self.get_answer("What is the tool?", context).strip()
        return {"heading": heading, "target": target, "tool": tool}
