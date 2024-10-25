import streamlit as st
import requests
import json
import time

# Define API Key and Base URL
API_KEY = "tauHGktuvULkGzYof5jKdVCNfZZryj32"
API_BASE_URL = "https://oapi.tasking.ai/v1"
MODEL_ID = "X5lMcszUYZvPpFnigD8mCfPI"

# Streamlit interface setup
st.set_page_config(page_title="Custom Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI-Buddy Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# Function to make a request to the custom API
def get_chat_response():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    data = {
        "model": MODEL_ID,
        "messages": st.session_state.messages  # Send the entire message history
    }

    try:
        response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=data)
        
        if response.status_code == 200:
            # Parse the response as JSON
            response_json = response.json()

            # Extract the content from the response
            content = response_json["choices"][0]["message"]["content"]

            # Try to parse the content if it's a valid JSON string
            try:
                content_parsed = json.loads(content)
                # If content is a valid JSON, extract the final message
                return content_parsed["choices"][0]["message"]["content"]
            except json.JSONDecodeError:
                # If content is not a valid JSON, return it as-is
                return content
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

    except Exception as e:
        # Log the error for internal use
        st.error("Re-enter the prompt")
        print(f"Error: {e}")
        return None

# Function to simulate streaming effect for displaying assistant's response
def display_response_streaming(response_content):
    response_placeholder = st.empty()  # Create an empty placeholder for the assistant's response
    streaming_text = ""
    for char in response_content:
        streaming_text += char
        response_placeholder.write(streaming_text)
        time.sleep(0.05)  # Small delay to simulate typing effect

# Chat interface
if prompt := st.chat_input("Type your message"):
    # Append user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat history and generate assistant response
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate assistant response if the last message is from the user
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get assistant's response based on the entire conversation history
            response_content = get_chat_response()
            if response_content:
                # Stream the assistant's response chunk by chunk
                display_response_streaming(response_content)
                # Append the assistant's response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": response_content})
            else:
                st.write("Sorry, Re-enter the prompt")
