from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OCR_ENGINE = os.getenv("OCR_ENGINE", "pytesseract")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
llm = ChatOpenAI(temperature=0)

def create_qa_chain(vector_store):
    return RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever(), return_source_documents=True)

def generate_theme_summary(docs):
    all_contents = "\n\n".join([doc.page_content + f" ({doc.metadata['source']})" for doc in docs])
    theme_prompt = f"""You are a document analyst. Given the following answers from multiple documents, identify common themes and summarize them clearly.

Answers:
{all_contents}

Give a bulleted list of themes with citations (if any)."""
    return llm.predict(theme_prompt)