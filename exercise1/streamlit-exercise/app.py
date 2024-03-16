import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="<your secret key>")

# Create a layout with 3 columns
col1, col2, col3 = st.columns([1, 2, 1])

# Display the logo in the left column
with col1:
    st.image("iabg_logo.png", width=100)  # Adjust width as necessary

# Display the title in the middle column. We attempt to center it by using Markdown & HTML
with col2:
    st.markdown("<h1 style='text-align: center;'>My Chatbot</h1>", unsafe_allow_html=True)


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

 # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})