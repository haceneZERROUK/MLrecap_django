# import os
# from dotenv import load_dotenv, find_dotenv
# import request
# import json



# dot_env_path = find_dotenv()
# load_dotenv(dotenv_path=dot_env_path)

# EMAIL = os.getenv("EMAIL", None)
# PASSWORD = os.getenv("PASSWORD", None)
# API_URL = os.getenv("API_URL", None)


# def get_token(api:str = API_URL, email:str = EMAIL, password:str = PASSWORD) -> dict: 
    
#     api_login_url = api+"/login/"
#     headers = {
#         "accept" : "application/json", 
#         "Content-Type" : "application/json"
#     }
#     data = {
#         "email" : email, 
#         "password" : password
#     }
#     token_response = request.post(url = api_login_url, headers = headers, data = data)
#     return token_response    


# def api_prediction(movie : dict, token:str = TOKEN, api:str = API_URL) -> dict: 
    
#     api_predict_url = api+"/predict/"
#     headers = {
#         "accept" : "application/json", 
#         "Content-Type" : "application/json", 
#         "Authorization" : f"Bearer{token}"
#     }
#     data = {**movie}
#     prediction_response = request.post(url = api_predict_url, headers = headers, data = data)
#     if prediction_response.code == 200 : 
#         return prediction_response
#     else : 
#         token = get_token()
#         headers = {
#             "accept" : "application/json", 
#             "Content-Type" : "application/json", 
#             "Authorization" : f"Bearer{token}"
#         }
#         prediction_response = request.post(url = api_predict_url, headers = headers, data = data)
#         return prediction_response
        
#     MOVIES_FILE = os.getenv("MOVIES_FILE_PATH", "niab/.env")
    
    
# def weekly_prediction(self) -> list : 
    
#     predictions = []
#     with open(self.MOVIES_FILE) as file : 
#         movies = json.load(file)
    
#     variables = ['fr_title', 'released_year', 'directors', 'writer', 'distribution', 'country', 'budget', 'category', 'released_date', 'classification', 'duration', 'weekly_entrances', 'duration_minutes', 'actor_1', 'actor_2', 'actor_3']
    
#     movies_with_preds = []
    
#     for m in movies : 
#         fr_title = m["fr_title"]
#         original_title = m["original_title"]
#         released_date = m["released_date"]
#         casting = [m["actor_1"], m["actor_2"], m["actor_3"]]
#         director = m["directors"]
#         writer = m["writer"]
#         distribution = m["distribution"]
#         country = m["country"]
#         classification = m["classification"]
#         duration = m["duration"]
#         categories = m["categories"]
#         synopsis = m["synopsis"]
#         image_url = m["image_url"]
#         allocine_url = m["allocine_url"]
        
#         pred_data = {v : m.get(v) for v in variables}
#         prediction = api_prediction(**pred_data)
#         weekly_entrances_pred = prediction
        
#         movies_with_preds.append({
#             "fr_title" : fr_title, 
#             "original_title" : original_title, 
#             "released_date" : released_date, 
#             "casting" : casting, 
#             "director" : director, 
#             "writer" : writer, 
#             "distribution" : distribution, 
#             "country" : country, 
#             "classification" : classification, 
#             "duration" : duration, 
#             "categories" : categories, 
#             "weekly_entrances_pred" : weekly_entrances_pred, 
#             "synopsis" : synopsis, 
#             "allocine_url" : allocine_url, 
#             "image_url" : image_url
#         })
        
#         movie_to_save = Movie(
#             fr_title = fr_title, 
#             original_title = original_title, 
#             released_date = released_date, 
#             casting = casting, 
#             director = director, 
#             writer = writer, 
#             distribution = distribution, 
#             country = country, 
#             classification = classification, 
#             duration = duration, 
#             categories = categories, 
#             weekly_entrances_pred = weekly_entrances_pred, 
#             synopsis = synopsis, 
#             allocine_url = allocine_url, 
#             image_url = image_url
#         )
#         movie_to_save.save()
    
#     return movies_with_preds

        

    














