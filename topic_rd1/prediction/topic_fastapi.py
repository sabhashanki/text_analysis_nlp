
# Importing fastapi modules
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Importing transformer modules
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

# Importing dependent modules for authentication and schemas
import auth_topic
import schema_topic

# Importing basic modules
from scipy.special import expit
import logging
import datetime
import configparser

logging.basicConfig(level=logging.INFO, filename='../topic.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Module Initialization
try:
    auth_handler = auth_topic.AuthHandler()
    MODEL = "./files"  # Keep the model files in the same directory
    TOKENIZER = "./files/roberta-base/"  # Keep the roberta-base folder in the same directory
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    class_mapping = model.config.id2label
    config = configparser.ConfigParser()
    config.read('./config_topic.ini')  # Keep config file in the same directory
    model_name = config['TOPIC']['MODEL_NAME']
    logging.info('Initialization Done')
except Exception:
    raise HTTPException(status_code=500, detail='INITIALIZATION FAILED')

#
# # Registration Endpoint
# @app.post('/v1.0/register', status_code=201)
# async def register(auth_details: schema_topic.AuthDetails):
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
# async def login(auth_details: schema_topic.AuthDetails):
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
async def read_text(data: schema_topic.Item, username=Depends(auth_handler.auth_wrapper)):
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
            content = {
                "post": data.text,
                "topic": prediction,
                "timestamp": time
            }
            content = jsonable_encoder(content)
            return JSONResponse(content)
        except Exception:
            raise HTTPException(status_code=500, detail='MODULE EXECUTION ERROR')
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <roberta-base-2019>')

