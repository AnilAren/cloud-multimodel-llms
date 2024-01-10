from Azure.azure_fe import make_api_request, get_payload
import streamlit as st
from icecream import ic
    
def Azure_param_slider():
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


def Azure_sidebar():
    # dropdown to select the model type
    selected_model = st.sidebar.selectbox("Select Option", ["GPT 3.5 Turbo", "GPT 4 - 32k"], index=0)
    if selected_model == "GPT 4 - 32k":
        url = "/azure/gpt-34-turbo/"
    else:
        url = "/azure/gpt-4-32k/"
        
    selected_option = st.sidebar.selectbox("Select Option", ["Text", "Chat"], index=0)

    temperature, top_p, max_tokens = Azure_param_slider()
    
    text = st.text_area("Enter your text here:")
    col1, col2,col3 = st.columns(3)
    with col1:
        text_submit_button = st.button("Submit")
    if text_submit_button:
        if text:
            payload = get_payload(text,max_tokens=max_tokens,top_p=top_p,temperature=temperature)
            if selected_option == "Text":
                response = make_api_request(url+"completion",payload)
            elif selected_option == "Chat":
                response = make_api_request(url+"chat-completion",payload)
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
            reset_response = make_api_request(url+"reset-conversation-history")
            if reset_response.status_code == 200:
                st.info("Chat reset successful.")
            else:
                st.error("Failed to reset chat. " + reset_response.json().get('message'))


def main():
    st.title("Welcome to GPT World!!!")

    left_navigation_sideBar()
    
        
if __name__ == '__main__':
    main()


