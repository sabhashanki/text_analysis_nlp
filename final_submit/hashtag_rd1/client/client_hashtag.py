
# Importing basic modules
import requests
import pandas as pd
import time

# Initialization
HOST_URL = "localhost"
API_VERSION = "v1.0"
PORT = 8001
sample_data_file = "../../sample.csv"


def client_script():

    # Prediction Module
    try:
        df = pd.read_csv(sample_data_file)
        for index, rows in df.iterrows():
            data = rows['text']
            result = requests.post(f'http://{HOST_URL}:{PORT}/{API_VERSION}/prediction',
                                   headers={'Content-type': 'application/json'},
                                   json={'text': data, 'model': 'openai'})
            if result.status_code == 201 or result.status_code == 200:
                print(result.json())
            if result.status_code == 401:
                print('YOUR API KEY IS INVALID,EXPIRED OR REVOKED')
            elif result.status_code == 429:
                print('MAXIMUM LIMIT REACHED, TRY AFTER SOMETIME')
                time.sleep(10)
            elif result.status_code == 503:
                print('ISSUE ON OPENAI SERVER - REFER https://status.openai.com/ FOR ANY SCHEDULED MAINTENANCE OR OUTAGE')
            elif result.status_code == 500:
                print('MODULE EXECUTION ERROR')
            elif result.status_code == 404:
                print('INVALID MODEL NAME')
    except:
        return 'CLIENT MODULE EXECUTION ERROR'


client_script()
