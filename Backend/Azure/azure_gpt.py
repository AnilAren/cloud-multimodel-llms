from Azure.LLM_Config import Azure_gpt_config

from flask import Flask, request, jsonify, Blueprint
from icecream import ic

Azure_GPT_Blueprint= Blueprint("Azure_GPT",__name__)

#==============================================COMPLETION/TEXT===============================================================
# we can create a common function to call both completion and chat completion as the only difference is how we are passing the msg --> not implementing this logic to make it more understandable

@Azure_GPT_Blueprint.route("/completion", methods=["POST"])  # Azure ==> text or completion API
def text_completion():
    try:
        data = request.get_json()
        model_name= data['model_name']
        # configure Azure LLM
        llm = Azure_gpt_config()
        print(llm)
        
        prompt = data['prompt']
        top_p = data['top_p']
        temperature = data['temperature']
        max_tokens = data['max_tokens']
        # creating response
        resp = llm.chat.completions.create(
            model= model_name,
            messages=[
                {
                "role": "user",
                "content": prompt,
            },
                ],
            temperature= temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        return resp.choices[0].message.content
    
    except Exception as e:
    # The HTTP status code 500 is a generic error response. It means that the server encountered an unexpected condition that prevented it from fulfilling the request.
        return jsonify({"status_code": 500, "status": "error", "message": str(e)})


#===================================Chat Completion====================================================================

conversation_history=[]

@Azure_GPT_Blueprint.route("/chat-completion", methods=["POST"])
def chat_completion(): # Chat Completion with chat history compatibility
    try:
        data = request.get_json()
        model_name= data['model_name']
        # configure Azure LLM
        llm = Azure_gpt_config()
        
        prompt = data.get('prompt')
        prompt = data['prompt']
        top_p = data['top_p']
        temperature = data['temperature']
        max_tokens = data['max_tokens']
        
        global conversation_history
        messages = conversation_history
        if not conversation_history:
            system_message = "You are a helpful assistant."
            messages = [{"role": "system", "content": system_message}]
        else:
            messages = conversation_history[:]
            
        messages = add_msg("user", prompt, messages)
        
        resp = llm.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature= temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        answer = resp.choices[0].message.content
        messages = add_msg("assistant", answer, messages)
        conversation_history = messages 
        ic(conversation_history)
        return answer
    except Exception as e:
        return jsonify({"status_code": 500, "status": "error", "message": str(e)})
    
def add_msg(role,data,msg):  # appending messages to the model message parameter
    msg.append({
            "role": role,
            "content": data,
        })
   
    return msg

#-----------------------------------------------------------------------------------------------
@Azure_GPT_Blueprint.route("/reset-conversation-history", methods=["POST"])
def reset_conversation_history(): # when we refresh the page the chat history remains so for fresh chat we need to reset the Chat history
    ic("going inside reset-conversation-history API")
    try:
        global conversation_history
        conversation_history = []  # Reset conversation history
        ic("successful reset in backend")
        return {"status_code":"200", "status":"success", "message": "Conversation history reset."}
    except Exception as e:
        return {"status_code": 500, "status": "error", "message": str(e)}
    finally:
        ic("Exiting from reset-conversation-history API")
    
#=============================================================================================================