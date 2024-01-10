Why POST not GET when calling LLM?
- When working with OpenAI's GPT models or other Language Models, API requests that involve generating text or processing large input data (such as conversation history for chat-based models) often use POST requests. This is because the input data may be large, and including it in the request body is more practical and secure.
- 1--> if we use GET it will become large URL 2-> POST is more secure since for get the data of request is in the  URL

Azure:
    Used singleton when creating Azure LLM

    -- we are taking 3 parameters 
        1. top_p
        2. temperature
        3. max_tokens
    -- .env prefix :
        for gpt 3.4 turbo --> Azure_GPT_4_32k
            gpt 4 32k --> Azure_GPT_35_turbo