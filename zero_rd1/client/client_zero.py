
# Importing basic modules
import requests
import pandas as pd

# Initialization
HOST_URL = "localhost"
API_VERSION = "v1.0"
sample_data_file = "../../sample.csv"
credentials = {'username': 'khulke', 'password': 'aifylabs'}


def client_script():
    # Register Module
    try:
        register = requests.post(f'http://{HOST_URL}:8001/{API_VERSION}/register',
                                 headers={'Content-type': 'application/json'},
                                 json=credentials
                                 )
        if register.status_code == 400:
            print(f'USER ALREADY REGISTERED - TRY DIFFERENT USERNAME')
        elif register.status_code == 201:
            print(f'USERNAME: {credentials["username"]} CREATION : SUCCESS')
    except:
        return 'REGISTRATION ERROR - TRY AGAIN'

    # Login Module
    try:
        token = requests.post(f'http://{HOST_URL}:8001/{API_VERSION}/login',
                              headers={'Content-type': 'application/json'},
                              json=credentials
                              )
        if token.status_code == 401:
            print('INVALID USERNAME/PASSWORD')
        elif token.status_code == 500:
            print('TOKEN GENERATION FAILED')
        elif token.status_code == 201:
            token = token.text[1:-1]
            print(f'USER : {credentials["username"]} LOGGED IN - TOKEN VALID FOR 20 MINUTES')
    except:
        return 'LOGIN ERROR'

    # Prediction Module
    try:
        df = pd.read_csv(sample_data_file)
        t = []
        for index, rows in df.iterrows():
            data = rows['text']
            result = requests.post(f'http://{HOST_URL}/{API_VERSION}/prediction',
                                   headers={'Authorization': f'Bearer {token}', 'Content-type': 'application/json'},
                                   json={'data': data, 'model': 'zero-shot',
                                         'labels': ['sports', 'crime', 'food', 'travel', 'polity', 'health',
                                                    'governance', 'celebrity', 'philosophy', 'arts', 'business',
                                                    'economy', 'entertainment', 'faiths', 'languages', 'lifystyle',
                                                    'places', 'science and technology', 'social media', 'world affair']}
                                   )
            if result.status_code == 201 or result.status_code == 200:
                print(result.json())
            if result.status_code == 401:
                print('TOKEN EXPIRED')
            if result.status_code == 498:
                print('INVALID TOKEN')
            elif result.status_code == 500:
                print('MODULE EXECUTION ERROR')
            elif result.status_code == 404:
                print('INVALID MODEL NAME')
    except:
        print('CLIENT MODULE EXECUTION ERROR')


client_script()