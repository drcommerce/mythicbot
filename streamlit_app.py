import streamlit as st
import requests
import json

# API Key and URL (replace with your actual values)
API_KEY = "2GxdA3IT.2RIPThfls0aRk35SESK16n0KHouq4y1t"
URL = "https://payload.vextapp.com/hook/48PJ2KFJVI/catch/ML"


def call_vext_api(payload):
    """
    Function to call the Vext RAG model API using requests,
    with error handling for the response.
    """
    headers = {"Content-Type": "application/json", "Apikey": f"Api-Key {API_KEY}"}
    data = {"payload": payload}
    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        try:
            # Attempt to access the "response" key
            return response.json()["response"]
        except KeyError:
            # Handle the case where "response" key is missing
            return "Error: Unexpected response format from Vext API."
    else:
        return f"Error: {response.status_code}"


# Show title and description.
st.title(" Chatbot")
st.write(
    "1. This is a simple chatbot that uses your Vext Retrieval-Augmented Generation (RAG) model. "
    "Ensure you have the Vext RAG model API running and accessible."
)

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the Vext RAG model API function.
    response = call_vext_api(prompt)

    # Display the response using `st.write`.
    with st.chat_message("assistant"):
        st.write(response.txt)

    # Store the response in session state (optional)
    # st.session_state.messages.append({"role": "assistant", "content": response})
