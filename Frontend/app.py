from azure_fe import (
    make_api_request,
    get_payload, 
    azure_chat_completion_url,
    azure_completion_url,
    azure_reset_chat_history_url,
    azure_image_generation_url,
    aws_invoke_llm_url)

import streamlit as st
from icecream import ic

def param_slider():
    st.sidebar.header("Parameters")
    temperature = st.sidebar.slider(label="Temperature",min_value=0.0,max_value=1.0,step=0.1)
    
    top_p = st.sidebar.slider(label="Top probabilities | Top_p",min_value=0.0,max_value=1.0,step=0.1)
    
    max_tokens= st.sidebar.slider(label="Max Tokens",min_value=1,max_value=4000,step=1,value=1000)
    
    return temperature, top_p, max_tokens

# Define functions for left navigation and main content
def left_navigation_sideBar():
    st.sidebar.header("Hello!!!")
    st.sidebar.header("Select the LLM Model")
    cloud_service_provider =st.sidebar.selectbox("Please choose the Cloud Service Provider",
    ("Azure", "AWS", "GCP"))
    
    if cloud_service_provider == "Azure":
        Azure_sidebar()
    elif cloud_service_provider =="AWS":
        Aws_sidebar()
        
        
def Aws_sidebar():
    
    selected_type = st.sidebar.selectbox("Select Option", ["Cohere" ,"Anthropic","AI21","Meta"], index=0)
    if selected_type == 'Cohere':
        selected_model = "cohere.command-text-v14" 
    elif selected_type == "Anthropic":
        selected_model = st.sidebar.selectbox("Select Option", ["anthropic.claude-v1", "anthropic.claude-v2","anthropic.claude-instant-v1"])
    elif selected_type == "AI21":
        selected_model = st.sidebar.selectbox("Select Option", ["ai21.j2-ultra-v1", "ai21.j2-mid-v1"])
    elif selected_type == "Meta":
        selected_model = "meta.llama2-13b-chat-v1"
    text = st.text_area("Enter your text here:")
    col1, col2,col3 = st.columns(3)
    with col1:
        text_submit_button = st.button("Submit")
    temperature, top_p, max_tokens = param_slider()
    if text_submit_button:
            if text:
                payload = get_payload(text,model_name=selected_model,max_tokens=max_tokens,top_p=top_p,temperature=temperature)
                response = make_api_request(aws_invoke_llm_url,payload)
                st.subheader("AI Response:")
                print(type(response.json()))
                resp = response.json()
                st.info(resp['content'])

def Azure_sidebar():
    # dropdown to select the model type
    selected_type = st.sidebar.selectbox("Select Option", ["Generative Model", "Image Generative Model"], index=0)
    if selected_type == "Generative Model":
        selected_model = st.sidebar.selectbox("Select Option", ["gpt-35-turbo", "gpt-4"], index=0)    
        selected_option = st.sidebar.selectbox("Select Option", ["Text", "Chat"], index=0)

        temperature, top_p, max_tokens = param_slider()
        
        text = st.text_area("Enter your text here:")
        col1, col2,col3 = st.columns(3)
        with col1:
            text_submit_button = st.button("Submit")
        if text_submit_button:
            if text:
                payload = get_payload(text,model_name = selected_model,max_tokens=max_tokens,top_p=top_p,temperature=temperature)
                if selected_option == "Text":
                    response = make_api_request(azure_completion_url,payload)
                elif selected_option == "Chat":
                    response = make_api_request(azure_chat_completion_url,payload)
                st.subheader("AI Response:")
                st.info(response.text)
    
        if selected_option == "Chat":
            # New Chat button
            with col3:
                col3_1,col3_2 = st.columns([1,1])
                with col3_2:
                    new_chat_button = st.button("New Chat")
                
            # Check if the new chat button is pressed
            if new_chat_button:
                reset_response = make_api_request(azure_reset_chat_history_url)
                if reset_response.status_code == 200:
                    st.info("Chat reset successful.")
                else:
                    st.error("Failed to reset chat. " + reset_response.json().get('message'))


    elif selected_type == "Image Generative Model":
        selected_model = st.sidebar.selectbox("Select Option", ["DALL-E-2"], index=0)
        url = "/azure/image/"
        text = st.text_area("Enter your propmt here:")
        col1, col2,col3 = st.columns(3)
        with col1:
            text_submit_button = st.button("Submit")
            
        if text_submit_button:
            payload=get_payload(text)
            image_url = make_api_request(azure_image_generation_url,payload)
            image_response=image_url.json()
            #response.json()['status']
            if image_response['status'] == "succeeded":    
                img=image_response['result']['data'][0]['url']
                st.image(img, caption=text, use_column_width=True)
            else:
                st.error(image_response['error'])
    

def main():
    st.title("Welcome to GPT World!!!")

    left_navigation_sideBar()
    
        
if __name__ == '__main__':
    main()


