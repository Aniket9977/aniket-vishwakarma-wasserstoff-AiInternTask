import streamlit as st
import requests

st.set_page_config(page_title="Document Chatbot", layout="wide")
st.title("📚 Document Research & Theme Chatbot")

API_URL = "http://localhost:8000"

# --- Upload documents ---
st.header("1️⃣ Upload Documents")

uploaded_files = st.file_uploader("Upload PDF/Image/Text files", type=["pdf", "txt", "jpg", "jpeg", "png"], accept_multiple_files=True)

if st.button("Upload"):
    if uploaded_files:
        for file in uploaded_files:
            files = {"file": (file.name, file.getvalue())}
            response = requests.post(f"{API_URL}/upload/", files=files)
            if response.status_code == 200:
                st.success(f"Uploaded: {file.name}")
            else:
                st.error(f"Failed to upload {file.name}")
    else:
        st.warning("Please upload at least one file.")

# --- Ingest vectorstore ---
st.header("2️⃣ Create Vectorstore")

if st.button("Create Knowledge Base"):
    response = requests.post(f"{API_URL}/ingest/")
    if response.status_code == 200:
        st.success("Vectorstore created successfully!")
    else:
        st.error("Error during ingestion!")

# --- Ask a question ---
st.header("3️⃣ Ask a Question")

query = st.text_input("Ask something about the uploaded documents")

if st.button("Get Answer"):
    if query:
        response = requests.post(f"{API_URL}/query/", json={"question": query})
        if response.status_code == 200:
            result = response.json()
            st.markdown("### 💡 Answer")
            st.write(result["answer"])
        else:
            st.error("Failed to get an answer.")
    else:
        st.warning("Please enter a question.")
