
# Importing fastapi modules
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Importing KeyBERT modules
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer

# Importing dependent modules for schemas
from utils import Item

# Importing basic modules
import logging
import datetime
import configparser
import sys
import nltk
nltk.data.path.append("./files/nltk_data")


logging.basicConfig(level=logging.INFO, filename='./keyword.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Module Initialization
try:

    # Keybert module
    kw_extractor = KeyBERT('./files')  # Keep model files in the same directory
    
    # config parser
    config = configparser.ConfigParser()
    config.read('./config_keyword.ini')  # Keep config file in the same directory
    limit = int(config['KEYWORD']['OUTPUT_LIMIT'])
    threshold_range = float(config['KEYWORD']['THRESHOLD_RANGE'])
    model_name = config['KEYWORD']['MODEL_NAME']
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

            logging.info('Keyword module execution')
            keywords = kw_extractor.extract_keywords(data.text, vectorizer=KeyphraseCountVectorizer(), stop_words=None,
                                                     top_n=limit)
            keywords = [i for i in keywords if i[1] > threshold_range]
            keybert_diversity_phrases = []
            for i, j in keywords:
                keybert_diversity_phrases.append(i)
            content = {'Post': data.text, 'Keywords': keybert_diversity_phrases[:limit], 'timestamp': time}
            content = jsonable_encoder(content)
            logging.info('Returning output')
            return JSONResponse(content)
        
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='MODULE EXECUTION ERROR')
  
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <mini-lm>')
