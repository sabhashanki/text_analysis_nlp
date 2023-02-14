
# Importing fastapi modules
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Importing openai modules
import openai

# Importing dependent modules for authentication and schemas
import auth_hashtag
import schema_hashtag

# Importing basic modules
import datetime
import logging
import os
import sys

# Importing environment and configuration modules
from dotenv import load_dotenv
import configparser

logging.basicConfig(level=logging.INFO, filename='hashtag.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Module Initialization
try:
    auth_handler = auth_hashtag.AuthHandler()
    config = configparser.ConfigParser()
    config.read("./config_hashtag.ini")
    temp = float(config['HASHTAG']['TEMPERATURE_PARAMETER'])
    max_tok = int(config['HASHTAG']['MAX_TOKEN_PARAMETER'])
    top_para = int(config['HASHTAG']['TOP_P_PARAMETER'])
    freq = int(config['HASHTAG']['FREQUENCY_PENALTY_PARAMETER'])
    presence = int(config['HASHTAG']['PRESENCE_PENALTY_PARAMETER'])
    model_name = config['HASHTAG']['MODEL_NAME']
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')  # store in .env file as API_KEY = "xxxxxx"
except Exception:
    raise HTTPException(status_code=500, detail='INITIALIZATION FAILED')


# Registration Endpoint
# @app.post('/v1.0/register', status_code=201)
# async def register(auth_details: schema_hashtag.AuthDetails):
#     df = pd.read_json('db.json', lines=True)
#     if any(x == auth_details.username for x in df.username):
#         raise HTTPException(status_code=400, detail=f'USER ALREADY REGISTERED - TRY DIFFERENT USERNAME')
#     logging.info('Username availability check')
#     hashed_password = auth_handler.get_password_hash(auth_details.password)
#     logging.info('Password Hashing')
#     df.loc[len(df.index)] = [auth_details.username, hashed_password]
#     df.to_json('db.json', orient='records', lines=True)
#     return f'REGISTRATION SUCCESSFUL: {bool(1)}'
#
#
# # Login Endpoint
# @app.post('/v1.0/login', status_code=201)
# async def login(auth_details: schema_hashtag.AuthDetails):
#     df = pd.read_json('db.json', lines=True)
#     user = None
#     logging.info('Username Authentication')
#     for index, row in df.iterrows():
#         if row['username'] == auth_details.username:
#             user = row['username']
#             password = row['password']
#             break
#     if (user is None) or (not auth_handler.verify_password(auth_details.password, password)):
#         raise HTTPException(status_code=401, detail='INVALID USERNAME/PASSWORD')
#     try:
#         token = auth_handler.encode_token(user)
#         logging.info('token generation')
#     except Exception:
#         raise HTTPException(status_code=500, detail='TOKEN GENERATION FAILED')
#     return token


# Prediction Endpoint
@app.post("/v1.0/prediction")
async def read_text(data: schema_hashtag.Item, username=Depends(auth_handler.auth_wrapper)):
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
            result = (original_result['choices'][0]['text'])
            result = result.replace('#', '')
            result = result.replace('\n', ' ')
            result = [i.strip() for i in result.split(' ')]
            result = [i for i in result if i != '']
            content = {'original': original_result, 'Post': data.text, 'hashtag': set(result), 'timestamp': time,
                       "consumed_tokens": int(original_result["usage"]["total_tokens"]),
                       "prompt_tokens":  int(original_result["usage"]["prompt_tokens"]),
                       "completion_tokens": int(original_result["usage"]["completion_tokens"])
                       }
            content = jsonable_encoder(content)
            return JSONResponse(content)
        except openai.error.RateLimitError:
            raise HTTPException(status_code=429, detail='MAXIMUM LIMIT REACHED, TRY AFTER SOMETIME')
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='MODULE EXECUTION ERROR')
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <openai>')


