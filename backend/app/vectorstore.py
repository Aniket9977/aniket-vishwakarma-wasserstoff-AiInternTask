from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vectorstore(text_chunks, persist_dir="db"):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(text_chunks, embeddings, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb
