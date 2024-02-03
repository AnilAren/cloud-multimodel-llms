!(pic1.png)

Why POST not GET when calling LLM?
- When working with OpenAI's GPT models or other Language Models, API requests that involve generating text or processing large input data (such as conversation history for chat-based models) often use POST requests. This is because the input data may be large, and including it in the request body is more practical and secure.
- 1--> if we use GET it will become large URL 2-> POST is more secure since for get the data of request is in the  URL


Git Commit Standards:
    - feat– feature
    - fix– bug fixes
    - docs– changes to the documentation like README
    - style– style or formatting change 
    - perf – improves code performance
    - test– test a feature


why am I using .json in streamlit app --> as i am getting a http response  --> When you make an HTTP request to an API and receive a response, you can use the .json() method to parse the response content if it is in JSON format. This is a convenient way to convert the JSON-formatted data in the response to a Python object (usually a dictionary or a list).

  
Azure:
    - Utilizing both GPT-3.5-Turbo and GPT-4-32k models from Azure OpenAI
    - will be using singleton architecute when creating LLM Objects so that the object and client are created only once
    
    -- we are taking 3 parameters for our LLMs
        1. top_p
        2. temperature
        3. max_tokens

    -- we have different keys for GPT-3.5-Turbo and GPT-4-32k models so we are gonnna store the keys in the .env with a prefix
        -->.env prefix :
                - for gpt 3.4 turbo --> Azure_GPT_4_32k
                -    gpt 4 32k --> Azure_GPT_35_turbo


For image
 we use gpt3.5 api keys and endpoint 
 api version is differnt for the image generation so we took a new env variable --> AZURE_IMAGE_GENERATOR_API_VERSION


 AWS:
    - we are using boto3 client
    - What is Boto3 --> Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python. It allows developers to interact with various AWS services using Python code. With Boto3, you can programmatically create, configure, and manage AWS resources

    I am writing aws adapter in a different way compared to Azure
    - i will be using OOP for Aws --> we have 4 models in Aws we want to work with 
        - Cohere 
            - cohere.command-text-v14
        - Anthropic
            - anthropic.claude-v1
            - anthropic.claude-v2
            - anthropic.claude-instant-v1
        - AI21
            - ai21.j2-ultra-v1
            - ai21.j2-mid-v1
        - Meta
            - meta.llama2-13b-chat-v1

            we go and create a seperate methods for each model and call them using invoke method and invoke will be accessed by the object and remaining will be private methods
            we will implement singleton here as well to get single client and object for every creation of the object

            
