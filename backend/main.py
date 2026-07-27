# app.py (Your Streamlit Cloud app)
import streamlit as st
import requests
import os
from requests.exceptions import ConnectionError, RequestException

st.set_page_config(page_title="Document Chatbot", layout="wide")
st.title("Document Research System")


API_URL = os.getenv("API_URL", "http://3.111.35.114:8000")


@st.cache_data(ttl=30)
def check_api_connection():
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, str(e)

# Sidebar with connection status
with st.sidebar:
    
    st.header(" System Status")
    st.info(f"**Backend:** {API_URL}")
    
    is_connected, api_info = check_api_connection()
    if is_connected:
        st.success(" Backend Connected")
        if api_info:
            st.json(api_info)
    else:
        st.error("Backend Disconnected")
        st.error(f"Error: {api_info}")
    
    if st.button(" Refresh"):
        st.cache_data.clear()
        st.rerun()

# Main app logic
if not is_connected:
    st.error("""
     **Backend Service Unavailable**
    
    Cannot connect to the backend API. Please:
    1. Check if the backend service is running on EC2
    2. Verify the API URL is correct
    3. Check AWS security group settings
    """)
    st.stop()

# --- Upload documents ---
st.header("Upload Documents")

uploaded_files = st.file_uploader(
    "Upload PDF/Image/Text files", 
    type=["pdf", "txt", "jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if st.button("Upload"):
    if uploaded_files:
        progress_bar = st.progress(0)
        success_count = 0
        
        for i, file in enumerate(uploaded_files):
            try:
                files = {"file": (file.name, file.getvalue())}
                response = requests.post(f"{API_URL}/upload/", files=files, timeout=60)
                
                if response.status_code == 200:
                    st.success(f" Uploaded: {file.name}")
                    success_count += 1
                else:
                    st.error(f" Failed to upload {file.name}")
                    
            except ConnectionError:
                st.error(" Connection error. Backend not accessible.")
                break
            except Exception as e:
                st.error(f" Error: {str(e)}")
                
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        st.info(f"Upload complete: {success_count}/{len(uploaded_files)} files")
    else:
        st.warning(" Please upload at least one file.")

# --- Ingest vectorstore ---
st.header("Create Vectorstore")

if st.button("Create Knowledge Base"):
    try:
        with st.spinner("Creating knowledge base..."):
            response = requests.post(f"{API_URL}/ingest/", timeout=120)
            if response.status_code == 200:
                st.success(" Vectorstore created successfully!")
            else:
                st.error(" Error during ingestion!")
    except Exception as e:
        st.error(f" Error: {str(e)}")

# --- Ask a question ---
st.header(" Ask a Question")

query = st.text_input("Ask something about the uploaded documents")

if st.button("Get Answer"):
    if query:
        try:
            with st.spinner("Getting answer..."):
                response = requests.post(f"{API_URL}/query/", json={"question": query}, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    st.markdown("###  Answer")
                    st.write(result["answer"])
                    
                    if "sources" in result:
                        with st.expander("📚 Sources"):
                            for source in result["sources"]:
                                st.write(f"• {source}")
                else:
                    st.error(" Failed to get an answer.")
        except Exception as e:
            st.error(f" Error: {str(e)}")
    else:
        st.warning(" Please enter a question.")