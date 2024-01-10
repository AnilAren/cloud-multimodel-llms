import requests
from icecream import ic
Azure_endpoint = "http://127.0.0.1:8080/"

def get_payload(question,**kwargs):
    payload = {"question": question,
               **kwargs}
    return payload

def make_api_request(endpoint,payload={}):
    ic(payload)
    api_url = Azure_endpoint + endpoint
    ic("api getting called from streamlit",api_url)
    response = requests.post(api_url, json=payload)
    return response
 
    
# def get_completion(payload):
#     api_url = Azure_endpoint+"completion"
#     payload = payload
#     response = requests.post(api_url, json=payload)
#     ic(response)
#     return response.text

# def get_chat_completion(payload):
#     api_url = Azure_endpoint+"chat-completion"
#     payload = payload
#     response = requests.post(api_url, json=payload)
#     ic(response)
#     return response.text

# def reset():
#     ic("inside rest in streamlit")
#     api_url = Azure_endpoint+"reset-conversation-history"
#     response = requests.post(api_url)
#     ic("reset",response)
#     return response