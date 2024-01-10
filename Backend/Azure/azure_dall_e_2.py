from Azure.LLM_Config import Azure_gpt_config
import os
from flask import Flask, request, jsonify, Blueprint
import requests
import time

Azure_image_genration_Blueprint= Blueprint("Azure_image_generator",__name__)

@Azure_image_genration_Blueprint.route("/image-generate",  methods=["POST"])
def image_generator():
    try:
        req_body = request.get_json()
        print(req_body)
        prompt = req_body['prompt']
        api_endpoint = os.getenv('Azure_GPT_35_turbo_OPENAI_API_BASE')
        api_version = os.getenv('AZURE_IMAGE_GENERATOR_API_VERSION')
        api_key = os.getenv('Azure_GPT_35_turbo_OPENAI_API_KEY')
        
        url = f"{api_endpoint}openai/images/generations:submit?api-version={api_version}"
        headers = {"api-key":api_key, "Content-type": "application/json"}
        body = {
            "prompt":prompt,    # Enter your prompt text here
            "size":'1024x1024',
            "n":1
            }
        
        submission = requests.post(url,headers=headers, json=body)
        operation_location = submission.headers["Operation-Location"]
        status =""
        while status!="succeeded":
            time.sleep(3)
            response = requests.get(operation_location, headers=headers)
            status = response.json()['status']
        return response.json() # we must pass it in this way or else it will throw an error

    except Exception as e:
        print(e)
        return e