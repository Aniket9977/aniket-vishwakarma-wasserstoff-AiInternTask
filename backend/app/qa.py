from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnableLambda
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI

def query_vectorstore(question, persist_dir="db"):
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=OpenAIEmbeddings())
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = OpenAI(temperature=0.3)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    result = qa.invoke(question)
    return result
