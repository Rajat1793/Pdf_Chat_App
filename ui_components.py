import streamlit as st

def set_theme():
    st.markdown(
        """
        <style>
        .mode-toggle {
            position: absolute;
            top: 10px;
            right: 20px;
            z-index: 9999;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    mode = st.radio("Theme", ["Light", "Dark"], horizontal=True, key="theme_toggle", label_visibility="collapsed")

    if mode == "Dark":
        st.markdown(
            """
            <style>
            body, .stApp {
                background-color: #0e1117 !important;
                color: #fafafa !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            body, .stApp {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

def layout_sidebar():
    st.header("Upload & Process")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    process_button = st.button("Process PDF", disabled=not uploaded_file)
    chat_button = st.button("Chat with Me", disabled=True)
    return uploaded_file, process_button, chat_button
