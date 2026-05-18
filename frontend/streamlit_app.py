import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Offline ChatGPT")

st.title("Offline ChatGPT")

# =========================
# CHAT SESSION SETUP
# =========================

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Chats")

# New chat button
if st.sidebar.button("+ New Chat"):

    st.session_state.chat_id = str(uuid.uuid4())

    st.session_state.messages = []

    st.rerun()

# =========================
# RECENT CHATS
# =========================

try:

    chats_response = requests.get(
        "http://127.0.0.1:8000/chats"
    )

    chats = chats_response.json()

    for chat in chats:

        if st.sidebar.button(chat[:8]):

            st.session_state.chat_id = chat

            history_response = requests.get(
                f"http://127.0.0.1:8000/chat-history/{chat}"
            )

            st.session_state.messages = history_response.json()

            st.rerun()

except:
    st.sidebar.warning("Could not load chats")

# =========================
# PDF Upload
# =========================

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file:

    with st.sidebar:

        with st.spinner("Processing PDF..."):

            response = requests.post(
                "http://127.0.0.1:8000/upload-pdf",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "application/pdf"
                    )
                }
            )

            st.success("PDF uploaded successfully!")

# =========================
# DISPLAY CHAT
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask something")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "chat_id": st.session_state.chat_id,
                "messages": st.session_state.messages
            },
            stream=True
        )

        for chunk in response.iter_content(chunk_size=None):

            if chunk:

                text = chunk.decode("utf-8")

                full_response += text

                response_placeholder.markdown(
                    full_response + "▌"
                )

        response_placeholder.markdown(full_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )
