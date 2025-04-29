import os
from dotenv import load_dotenv, find_dotenv, set_key
import requests
import json



dot_env_path = find_dotenv()
load_dotenv(dotenv_path=dot_env_path, override=True)

USERNAME = os.getenv("USERNAME", None)
EMAIL = os.getenv("EMAIL", None)
PASSWORD = os.getenv("PASSWORD", None)
API_URL = os.getenv("API_URL", None)


def get_token(api:str = API_URL, email:str = USERNAME, password:str = PASSWORD) -> dict: 
    
    api_login_url = api+"/login"
    headers = {
        "accept" : "application/json", 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {
        'grant_type': 'password',
        'username': email,
        'password': password,
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string'
    }
    token_response = requests.post(url = api_login_url, headers = headers, data = data)
    if token_response.status_code == 200:
        return token_response.json()["access_token"]
    else:
        try:
            detail = token_response.json().get("detail", token_response.text)
        except ValueError:
            detail = token_response.text
        raise Exception(f"Erreur API : {token_response.status_code} - {detail}")



def api_prediction(movie : list[dict], api:str = API_URL) -> dict: 
    
    TOKEN = os.getenv("ACCESS_TOKEN", None)
    api_predict_url = api+"/predictions"
    
    try :
        headers = {
            "accept" : "application/json", 
            "Content-Type" : "application/json", 
            "Authorization" : f"Bearer {TOKEN}"
        }
        
        response = requests.post(url = api_predict_url, headers = headers, json = movie)
        
        if response.status_code == 200 : 
            return response.json()["result"]
        
        else : 
            new_token = get_token()
            set_key(dot_env_path, "ACCESS_TOKEN", new_token, quote_mode="never")
            headers["Authorization"] = f"Bearer {new_token}"
            
            response = requests.post(url = api_predict_url, headers = headers, json=movie)
            if response.status_code == 200 :
                return response.json()["result"]
            else : 
                raise Exception(f"Erreur API : {response.status_code} - {response.text}")
        
    except Exception as e : 
        raise Exception(f"Erreur lors de la requête: {str(e)}")



if __name__ == "__main__" : 
    token = get_token()
    print(token)
    
    with open("niab/upcomes.json", "r") as file : 
        movies = json.load(file)
        
    pred = api_prediction(movies)
    print(len(pred))
    print(pred[0])