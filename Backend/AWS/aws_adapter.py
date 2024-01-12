import boto3 
import json
import os
from botocore.exceptions import ClientError
from icecream import ic
from dotenv import load_dotenv
load_dotenv()

Error_types = [
'AccessDeniedException',
'ResourceNotFoundException',
'ThrottlingException',
'InternalServerException',
'ValidationException',
'ServiceQuotaExceededException',
'ModelErrorException',
'ModelTimeoutException',
'ModelNotReadyException'
]


class AWSBedrockAdapter():
    """
    Desc:
        - Child class of the abstract Base Class - ModelRouterBase
        - implements the vendor specific model adapter for - AWSBedrock
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AWSBedrockAdapter, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.bedrock_client = boto3.client(service_name="bedrock-runtime",
                                           aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),    
                                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                            region_name=os.getenv('AWS_DEFAULT_REGION'))
 
    def __invoke_text(self, input_request, req_body):
        try:                
            if 'anthropic' in input_request['model_name']:
                req_body['prompt'] = "\n\nHuman:" + input_request["prompt"]+ "\n\nAssistant:"
               
            else:
                req_body['prompt'] = input_request['prompt']
 
            body = json.dumps(req_body)
            print(body)
            response = self.bedrock_client.invoke_model(
                body=body,
                modelId=input_request['model_name'],
                accept="application/json",
                contentType='application/json'        
            )
            print(response)
            response_body = json.loads(response.get('body').read())
                     
            if 'cohere' in input_request['model_name']:    
                content = response_body.get('generations')[0].get('text')            
            elif 'anthropic' in input_request['model_name']:
                content =  response_body.get("completion")
            elif 'ai21' in input_request['model_name']:
                content = response_body.get('completions')[0].get('data').get('text')            
            elif 'meta' in input_request['model_name']:
                content = response_body.get('generation')
           
            return {
                    "content" : content,
                    "status_code": str(response['ResponseMetadata']['HTTPStatusCode'])
                    }
    
 
        except ClientError as e:
            error_type = e.response['Error']['Code']
            if error_type in Error_types:
                status_code = e.response['ResponseMetadata']['HTTPStatusCode']
                description = e.response['Error']['Message']
                response = {
                        "status_code" : status_code,
                        "description"  : description
                        }  
                return response   
 
    def __cohere_invoke(self,req_msg):

        req_body = {}
        if 'parameters' in req_msg:
            if 'temperature' in req_msg:
                req_body['temperature'] = float(req_msg['temperature'])
            if 'top_p' in req_msg:
                req_body['p'] = float(req_msg['top_p'])
            if 'max_tokens' in req_msg:
                req_body['max_tokens'] = int(req_msg['max_tokens'])
            if 'top_k' in req_msg:
                req_body['k'] = int(req_msg['top_k'])            
    
        return self.__invoke_text(req_msg, req_body)                    

    def __ai21_invoke(self, input_request):
        req_body = {}
        if 'temperature' in input_request:
            req_body['temperature'] = float(input_request['temperature'])
        if 'top_p' in input_request:
            req_body['topP'] = float(input_request['top_p'])
        if 'max_tokens' in input_request:
            req_body['maxTokens'] = int(input_request['max_tokens'])            
       
        return self.__invoke_text(input_request, req_body)
   
    def __anthropic_invoke(self, input_request):
        req_body = {}
        if 'temperature' in input_request:
            req_body['temperature'] = float(input_request['temperature'])
        if 'top_p' in input_request:
            req_body['top_p'] = float(input_request['top_p'])
        if 'top_k' in input_request:
            req_body['top_k'] = int(input_request['top_k'])            
        req_body['max_tokens_to_sample'] = int(input_request.get('max_tokens', 100))

        return self.__invoke_text (input_request, req_body)
       
    def __meta_invoke(self,req_msg):
        req_body = {}
        
        if 'temperature' in req_msg:
            req_body['temperature'] = float(req_msg['temperature'])
        if 'top_p' in req_msg:
            req_body['top_p'] = float(req_msg['top_p'])
        if 'max_tokens' in req_msg:
            req_body['max_gen_len'] = int(req_msg['max_tokens'])          
    
        return self.__invoke_text(req_msg, req_body)  
       
    def invoke(self,req_msg):
        if type(req_msg) == str:
            req_msg = json.loads(req_msg)            
        if 'cohere' in req_msg['model_name']:
            print("working")
            return  self.__cohere_invoke(req_msg)
        elif 'ai21' in req_msg['model_name']:
            return  self.__ai21_invoke(req_msg)
        elif 'anthropic' in req_msg['model_name']:
            return  self.__anthropic_invoke(req_msg)
        elif 'meta' in req_msg['model_name']:
            return  self.__meta_invoke(req_msg)

if __name__ == '__main__':
    obj=AWSBedrockAdapter()
    req_msg = {
        'model_name': 'cohere.command-text-v14',
        'prompt' : "hi"
    }
    print(obj.invoke(req_msg))