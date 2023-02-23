
# Importing fastapi modules
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Importing dependent modules for schemas
from utils import Item

# Importing transformer module
import transformers

# Importing basic modules
import logging
import datetime
import sys
import configparser


logging.basicConfig(level=logging.INFO, filename='./zeroshot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Module Initialization
try:
    
    # zeroshot module
    try:
        classifier = transformers.pipeline("zero-shot-classification", model="./files", device = 0)  # Execute with GPU
    except:
        classifier = transformers.pipeline("zero-shot-classification", model="./files")  # Execute without GPU

    # config parser
    config = configparser.ConfigParser()
    config.read('./config_zero.ini')  # Keep config file in the same directory
    model_name = config['ZEROSHOT']['MODEL_NAME']
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

            logging.info('Zero-Shot module execution')
            post = data.data
            dynamic_labels = data.labels
            result = classifier(post, dynamic_labels)
            prediction = {}
            for label, score in zip(result['labels'], result['scores']):
                prediction[label] = score

            content = {
                'post': result['sequence'],
                'topic': prediction,
                'timestamp': time
            }
            content = jsonable_encoder(content)
            return JSONResponse(content)
        
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='MODULE EXECUTION ERROR')
        
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <zero-shot>')

