

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