import streamlit as st
from pdf_processing import process_pdf
from chat_handler import handle_chat
from ui_components import set_theme, layout_sidebar
from cache_logic import init_db, is_file_processed, mark_file_as_processed
import hashlib

# Initialize SQLite DB
conn, cursor = init_db()

# Layout
st.set_page_config(layout="wide")
st.title("PDF Chat Assistant")

# Dark/Light Mode Toggle
set_theme()

# Sidebar for upload and processing
uploaded_file, process_button, chat_button = layout_sidebar()

# Session state
if "chat_ready" not in st.session_state:
    st.session_state.chat_ready = False
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Process PDF
if uploaded_file and process_button:
    file_bytes = uploaded_file.getvalue()
    file_hash = hashlib.md5(file_bytes).hexdigest()

    if is_file_processed(cursor, file_hash):
        st.sidebar.info("File already processed.")
    else:
        vector_db = process_pdf(file_bytes, file_hash, uploaded_file.name)
        mark_file_as_processed(cursor, file_hash, uploaded_file.name)
        st.sidebar.success("PDF processed and indexed!")

    st.session_state.vector_db = vector_db
    st.session_state.chat_ready = True

# Enable chat button after processing
if st.session_state.chat_ready:
    st.sidebar.button("Chat with Me", key="chat_enabled", disabled=False)

# Chat interface
if st.session_state.chat_ready:
    handle_chat()
