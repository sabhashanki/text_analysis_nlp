
# Importing fastapi modules
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Importing transformer modules
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

# Importing dependent modules for authentication and schemas
from utils import Item

# Importing basic modules
from scipy.special import expit
import logging
import sys
import datetime
import configparser


logging.basicConfig(level=logging.INFO, filename='./topic.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Module Initialization
try:

    # Topic module
    MODEL = "./files"  # Keep the model files in the same directory
    TOKENIZER = f'{MODEL}/roberta-base/'  # Keep the roberta-base folder in the same directory
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    class_mapping = model.config.id2label

    # config parser
    config = configparser.ConfigParser()
    config.read('./config_topic.ini')
    model_name = config['TOPIC']['MODEL_NAME']
    logging.info('Initialization Done')

except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code=500, detail='INITIALIZATION FAILED')



# Prediction Endpoint
@app.post("/v1.0/prediction")
async def read_text(data: Item):

    if data.model == model_name:
        time = datetime.datetime.now()

        try:

            logging.info('Topic module execution')
            tokens = tokenizer(data.text, return_tensors='pt')
            output = model(**tokens)
            scores = output[0][0].detach().numpy()
            scores = expit(scores)
            pred_list = scores.tolist()
            prediction = {}
            for pos, score in enumerate(pred_list):
                prediction[class_mapping[pos]] = score
            sorted_prediction = dict(sorted(prediction.items(), key=lambda x : x[1], reverse=True))
            content = {
                "post": data.text,
                "topic": sorted_prediction,
                "timestamp": time
            }
            content = jsonable_encoder(content)
            return JSONResponse(content)
        
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='MODULE EXECUTION ERROR')
        
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <roberta-base>')

