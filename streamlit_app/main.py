"""
Streamlit UI for Adaptive RAG.
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Adaptive RAG",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Adaptive RAG with ChromaDB")

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Document Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt"],
        help="Upload a PDF or TXT file for RAG"
    )
    
    description = st.text_area(
        "Document Description",
        placeholder="Describe what this document is about...",
        help="This helps the system understand when to use this document"
    )
    
    if st.button("Upload Document", type="primary"):
        if uploaded_file and description:
            with st.spinner("Uploading and processing document..."):
                # Strip newlines from description for HTTP header
                clean_description = description.replace('\n', ' ').replace('\r', ' ').strip()
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                headers = {"X-Description": clean_description}
                response = requests.post(
                    f"{API_URL}/rag/documents/upload",
                    files=files,
                    headers=headers
                )
                if response.status_code == 200:
                    st.success("Document uploaded successfully!")
                else:
                    st.error(f"Upload failed: {response.text}")
        else:
            st.warning("Please provide both a file and description")

    st.divider()
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.header("💬 Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/rag/query",
                    json={"query": prompt}
                )
                if response.status_code == 200:
                    result = response.json()
                    answer = result["result"]["content"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error: {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except Exception as e:
                error_msg = f"Connection error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})