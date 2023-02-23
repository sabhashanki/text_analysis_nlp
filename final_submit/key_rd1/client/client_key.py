
# Importing basic modules
import requests
import pandas as pd

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
                                   json={'text': data, 'model': 'mini-lm'})
            if result.status_code == 201 or result.status_code == 200:
                print(result.json())
            elif result.status_code == 500:
                print('MODULE EXECUTION ERROR')
            elif result.status_code == 404:
                print('INVALID MODEL NAME')
    except:
        return 'CLIENT MODULE EXECUTION ERROR'


client_script()
