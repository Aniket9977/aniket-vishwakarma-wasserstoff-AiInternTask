from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OCR_ENGINE = os.getenv("OCR_ENGINE", "pytesseract")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def build_vector_store(texts, sources):
    docs = [
        Document(page_content=text, metadata={"source": source})
        for text, source in zip(texts, sources)
    ]
    embeddings = OpenAIEmbeddings()  # however you get your embedding model
    return FAISS.from_documents(docs, embeddings)

