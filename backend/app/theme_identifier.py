from openai import ChatCompletion

def identify_themes(docs, question):
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"Analyze the following information from multiple documents and summarize the main themes for the question:\n\nQuestion: {question}\n\n{context}"
    
    response = ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
