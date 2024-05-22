from typing import Dict

class NLPManager:
    def __init__(self):
        pass
    
    @staticmethod
    def convert_numbers(orig: str) -> str:
        numbers = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'niner': '9'
        }
        parts = orig.split()
        result = "".join(numbers.get(part, part) for part in parts)
        return result

    def qa(self, context: str) -> Dict[str, str]:
        context = context[0].lower() + context[1:]
        
        data_indices = {}
        
        for marker in ("heading", "target", "tool to deploy"):
            data_indices[marker] = context.index(marker + " is ")
            
        data_indices = dict(sorted(data_indices.items(), key=lambda item: item[1]))
        
        result = {}
        for i, (key, val) in enumerate(data_indices.items()):
            result[key] = context[val + len(key + " is "):(len(context) if (i == len(data_indices) - 1) else list(data_indices.items())[i + 1][1])]
            result[key] = result[key].strip().strip(',').strip(".")
            
        result["tool"] = result["tool to deploy"]
        del result["tool to deploy"]
        
        result["heading"] = NLPManager.convert_numbers(result["heading"])
        
        return result
