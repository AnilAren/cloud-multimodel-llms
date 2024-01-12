import requests
from icecream import ic
Azure_endpoint = "http://127.0.0.1:8080/"

azure_image_generation_url = "/azure/image/img"
azure_reset_chat_history_url = "/azure/reset-conversation-history"
azure_chat_completion_url = "/azure/chat-completion"
azure_completion_url = "/azure/completion"
aws_invoke_llm_url = "/aws/invoke"


def get_payload(question,**kwargs):
    payload = {"prompt": question,
               **kwargs}
    return payload


def make_api_request(endpoint,payload={}):
    ic(payload)
    api_url = Azure_endpoint + endpoint
    ic("api getting called from streamlit",api_url)
    response = requests.post(api_url, json=payload)
    return response
 