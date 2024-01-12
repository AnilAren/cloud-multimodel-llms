import os
from flask import request, Blueprint
import requests
import time

Azure_Image_Blueprint= Blueprint("Azure_image_generator",__name__)

# ===================================================================
# Failure Exception for Imgae Generation --> like " Your task failed as a result of our safety system "
class CustomAPIException(Exception):
    def __init__(self, error):
        self.error = error
        
# ==============================================================
@Azure_Image_Blueprint.route("/img",  methods=["POST"])
def image_generator():
    try:
        print("entering into image generation")
        
        req_body = request.get_json()
        
        print(req_body)
        
        prompt = req_body['prompt']
        
        api_endpoint = os.getenv('AZURE_IMAGE_OPENAI_API_BASE')
        api_version = os.getenv('AZURE_IMAGE_API_VERSION')
        api_key = os.getenv('AZURE_IMAGE_OPENAI_API_KEY')
        url = f"{api_endpoint}openai/images/generations:submit?api-version={api_version}"
        
        headers = {"api-key":api_key, "Content-type": "application/json"}
        
        body = {
            "prompt":prompt,    # Enter your prompt text here
            "size":'1024x1024',
            "n":1
            }
        
        print(body)
        submission = requests.post(url,headers=headers, json=body)
        
        operation_location = submission.headers["Operation-Location"]
        
        status =""
        while status!="succeeded"  and status!="failed":
            print("Image is fetting generated.. please wait ....")
            time.sleep(3)
            response = requests.get(operation_location, headers=headers)
            status = response.json()['status']
        if status == 'failed':
            raise CustomAPIException(response.json()['error']['message'])
        print("image url --->",response.json()['result']['data'][0]['url'])
        return response.json() # we must pass it in this way or else it will throw an error
    except CustomAPIException as custom_exception:
        print(custom_exception.error)
        return {"error" : custom_exception.error}
    except Exception as e:
        print(e)
        return {'error':e}