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

# Custom CSS to increase font size and make the sidebar interactive
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            font-size: 1.3rem;
            color: #333333;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content h1 {
            font-size: 1.8rem;
            font-weight: bold;
            color: #ff4b4b;
            margin-bottom: 15px;
        }
        .sidebar .sidebar-content select, .sidebar .sidebar-content textarea, .sidebar .sidebar-content input {
            border: 2px solid #ff4b4b;
            padding: 12px;
            font-size: 1.2rem;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .sidebar .sidebar-content button {
            background-color: #ff4b4b;
            color: white;
            font-size: 1.2rem;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .sidebar .sidebar-content button:hover {
            background-color: #ff6565;
        }
        .st-chat-message p {
            font-size: 1.3rem;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for AI in Profession
st.sidebar.title("Want to know how AI helps in your profession and the role of AI-Buddy?")
st.sidebar.write("Select your details below and discover the potential of AI in your career!")

# Dropdown options for profession with 'Other' option
professions = ["Software Engineer", "Data Scientist", "Marketing Specialist", "Financial Analyst", "Teacher", "Doctor", "Project Manager", "Consultant", "Business Analyst", "Other"]

# Dropdown options for field with 'Other' option
fields = ["IT", "Healthcare", "Education", "Finance", "Marketing", "Engineering", "Sales", "Human Resources", "Consulting", "Other"]

# Dropdowns for profession and field
profession = st.sidebar.selectbox("Choose Your Profession", professions)
field = st.sidebar.selectbox("Choose Your Field/Domain", fields)

# If 'Other' is selected, show a text input for custom entry
if profession == "Other":
    profession = st.sidebar.text_input("Please specify your profession")

if field == "Other":
    field = st.sidebar.text_input("Please specify your field")

# Text area for additional description
description = st.sidebar.text_area("About you (a short description)", placeholder="Briefly describe your role")

# Submit button
if st.sidebar.button("Submit"):
    # Add input details as a message to chat history
    st.session_state.messages.append(
        {"role": "user", "content": f"My profession is {profession} in the {field} field. Here’s a bit about me: {description}. Tell me how AI and AI-Buddy can help me."}
    )

# Initialize chat history
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
        "messages": st.session_state.messages  # Send entire conversation history
    }

    try:
        response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            content = response_json["choices"][0]["message"]["content"]

            try:
                content_parsed = json.loads(content)
                return content_parsed["choices"][0]["message"]["content"]
            except json.JSONDecodeError:
                return content
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error("Re-enter the prompt")
        print(f"Error: {e}")
        return None

# Function to simulate streaming effect for displaying assistant's response
def display_response_streaming(response_content):
    response_placeholder = st.empty()  # Create a placeholder for assistant's response
    streaming_text = ""
    for char in response_content:
        streaming_text += char
        response_placeholder.write(streaming_text)
        time.sleep(0.05)  # Small delay to simulate typing effect

# Chat interface - User Input
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
