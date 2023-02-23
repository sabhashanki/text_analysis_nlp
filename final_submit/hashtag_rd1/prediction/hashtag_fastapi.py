
# Importing fastapi modules
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
# Importing openai modules
import openai
# Importing dependent modules for authentication and schemas
from utils import postprocessing, Item
# Importing basic modules
import datetime
import logging
import os
import sys
# Importing environment and configuration modules
from dotenv import load_dotenv
import configparser


logging.basicConfig(level=logging.INFO, filename='./hashtag.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


app = FastAPI()

# Module Initialization
try:

    # config parser
    config = configparser.ConfigParser()
    config.read("./config_hashtag.ini")
    temp = float(config['HASHTAG']['TEMPERATURE_PARAMETER'])
    max_tok = int(config['HASHTAG']['MAX_TOKEN_PARAMETER'])
    top_para = int(config['HASHTAG']['TOP_P_PARAMETER'])
    freq = int(config['HASHTAG']['FREQUENCY_PENALTY_PARAMETER'])
    presence = int(config['HASHTAG']['PRESENCE_PENALTY_PARAMETER'])
    model_name = config['HASHTAG']['MODEL_NAME']

    # .env parser
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')  # store in .env file as API_KEY = "xxxxxx"

except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code=500, detail='INITIALIZATION FAILED')


# Prediction Endpoint
@app.post("/v1.0/prediction")
async def read_text(data: Item):
    if data.model == model_name:
        time = datetime.datetime.now()

        try:
    
            logging.info('Hashtag module execution')
            original_result = await openai.Completion.acreate(
                model="curie-instruct-beta",
                prompt=f"Given a tweet, suggest one most relevant hashtags for the tweet. List down each suggested hashtag in "
                       f"a separate line \nTweet:{data.text}\n",
                temperature=temp,
                max_tokens=max_tok,
                top_p=top_para,
                frequency_penalty=freq,
                presence_penalty=presence
            )

            result = postprocessing(original_result)
            content = {'Post': data.text, 'hashtag': set(result), 'timestamp': time,
                       "consumed_tokens": int(original_result["usage"]["total_tokens"]),
                       "prompt_tokens":  int(original_result["usage"]["prompt_tokens"]),
                       "completion_tokens": int(original_result["usage"]["completion_tokens"])
                       }
            content = jsonable_encoder(content)
            return JSONResponse(content)
        
        except openai.error.RateLimitError:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=429, detail='MAXIMUM LIMIT REACHED, TRY AFTER SOMETIME')
        except openai.error.AuthenticationError:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=401, detail='YOUR API KEY IS INVALID,EXPIRED OR REVOKED')
        except openai.error.ServiceUnavailableError:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=503, detail='ISSUE ON OPENAI SERVER - REFER https://status.openai.com/ FOR ANY SCHEDULED MAINTENANCE OR OUTAGE')
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=500, detail='MODULE EXECUTION ERROR')
        
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <openai>')


