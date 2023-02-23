
# Importing dependent packages
from pydantic import BaseModel

# Input schema
class Item(BaseModel):
    text: str
    model: str

# Postprocessing the raw output from OPENAI
def postprocessing(original_result):
    result = original_result['choices'][0]['text']
    result = result.replace('\n', ' ')
    result = [i.strip() for i in result.split(' ')]
    result = [i for i in result if i != '']
    result = [i.title() for i in result]
    return result