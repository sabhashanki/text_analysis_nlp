
# Importing fastapi modules
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Importing dependent modules for authentication and schemas
import auth_zero
import schema_zero

# Importing transformer module
import transformers

# Importing basic modules
import logging
import datetime
import configparser


logging.basicConfig(level=logging.INFO, filename='zero_shot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Module Initialization
try:
    try:
        classifier = transformers.pipeline("zero-shot-classification", model="./zero/", device=0)  # Execute with GPU
    except:
        classifier = transformers.pipeline("zero-shot-classification", model="./zero/")  # Execute without GPU
    auth_handler = auth_zero.AuthHandler()
    config = configparser.ConfigParser()
    config.read('./config_zero.ini')  # Keep config file in the same directory
    model_name = config['ZEROSHOT']['MODEL_NAME']
    logging.info('Initialization Done')
except Exception:
    raise HTTPException(status_code=500, detail='INITIALIZATION FAILED')

#
# # Registration Endpoint
# @app.post('/v1.0/register', status_code=201)
# async def register(auth_details: schema_zero.AuthDetails):
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
# async def login(auth_details: schema_zero.AuthDetails):
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
#


# Prediction Endpoint
@app.post("/v1.0/prediction")
async def read_text(data: schema_zero.Item, username=Depends(auth_handler.auth_wrapper)):
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
            raise HTTPException(status_code=500, detail='MODULE EXECUTION ERROR')
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <zero-shot>')

