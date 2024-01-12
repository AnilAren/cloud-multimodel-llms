from AWS.aws_adapter import AWSBedrockAdapter
from flask import Blueprint, request
from dotenv import load_dotenv
import logging
load_dotenv()

AWS_text_llm_Blueprint= Blueprint("aws_llm",__name__)

@AWS_text_llm_Blueprint.route("/invoke", methods = ['POST'])
def aws_llm_invoke():
    print(" -------------> Begin aws_llm_invoke")
    obj=AWSBedrockAdapter()
    req_msg = request.get_json()
    req_msg = {
        'model_name': req_msg['model_name'],
        'prompt' : req_msg['prompt']
    }
    response = obj.invoke(req_msg)
    print(response)
    return response