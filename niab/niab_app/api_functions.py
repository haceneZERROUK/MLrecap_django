import os
from dotenv import load_dotenv
import request
import json



dot_env_path = find_dotenv()
load_dotenv(dotenv_path=dot_env_path)

EMAIL = os.getenv("EMAIL", None)
PASSWORD = os.getenv("PASSWORD", None)
API_URL = os.getenv("API_URL", None)


def get_token(api:str = API_URL, email:str = EMAIL, password:str = PASSWORD) -> dict: 
    
    api_login_url = api+"/login/"
    headers = {
        "accept" : "application/json", 
        "Content-Type" : "application/json"
    }
    data = {
        "email" : email, 
        "password" : password
    }
    token_response = request.post(url = api_login_url, headers = headers, data = data)
    return token_response    


def api_prediction(movie : dict, token:str = TOKEN, api:str = API_URL) -> dict: 
    
    api_predict_url = api+"/predict/"
    headers = {
        "accept" : "application/json", 
        "Content-Type" : "application/json", 
        "Authorization" : f"Bearer{token}"
    }
    data = {**movie}
    prediction_response = request.post(url = api_predict_url, headers = headers, data = data)
    return prediction_response
    














