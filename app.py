import streamlit as st
from services.loader import extract_text_from_pdf, extract_text_from_image, extract_text_from_txt
from services.qa_engine import get_answer
from services.vector_store import build_vector_store

st.set_page_config(page_title="AI Research Assistant", layout="wide")

st.title("📄 Upload Document and Ask Questions")

uploaded_file = st.file_uploader("Upload a PDF / TXT / Image file", type=["pdf", "txt", "png", "jpg", "jpeg"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        texts, sources = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type.startswith("image/"):
        texts, sources = extract_text_from_image(uploaded_file)
    elif uploaded_file.type == "text/plain":
        texts, sources = extract_text_from_txt(uploaded_file)
    else:
        st.error("Unsupported file type")
        st.stop()

    st.success(" File processed. You can now ask questions!")

    vs = build_vector_store(texts, sources)

    question = st.text_input("Ask a question based on the uploaded document")

    if question:
        result = get_answer(vs, question)
        st.markdown("###  Answer")
        st.write(result["answer"])
        st.markdown("#### Sources")
        st.write(result.get("sources", "No sources found."))
