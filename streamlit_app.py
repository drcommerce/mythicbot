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
            # Access the text under the "text" key
            return response.json()["text"]
        except KeyError:
            return "Error: Unexpected response format from Vext API."
    else:
        return f"Error: {response.status_code}"


# Show title and description.
st.title("Mythos Chatbot")
st.write(
    "This is a chatbot that uses Facebook's opensource Llama LLM to generate answer questions about Mythic Legions Action Figures. \n"
    "\nTo use this app, Simply ask a question about Mythic Legions and wait for a response. \n"
    "\nFor example, you can ask: 'Who are the four horsemen in mythic legions?' or 'Tell me a story that takes place in the lands of Mythos.'"
)

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Append the new message to the session state
st.session_state.messages.append({"role": "assistant", "content": response})

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
        try:
            response = call_vext_api(prompt)
            st.write(response)
        except Exception as e:
            st.write(f"Error: {e}")

    # Store the response in session state (optional)
    # st.session_state.messages.append({"role": "assistant", "content": response})
