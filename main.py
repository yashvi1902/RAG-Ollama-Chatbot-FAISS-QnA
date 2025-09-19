from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

template = """
Answer the question below.

CSUF related information just for context and not to be referenced in the answer you give : {context}
Give Factual and quantitative precise answers and keep it brief.
Question : {question}

Answer : 
"""

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
faiss_store = FAISS.load_local("faiss_index_",embedding_model,allow_dangerous_deserialization=True )
# Initialize the Llama model using Ollama
llm = OllamaLLM(model="llama3.1",preload=True)


prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm


def handle_conv():
    print("Welcome to CSUF advising system! type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower()=="exit":
            break
        result = chain.invoke({"context": faiss_store.similarity_search(user_input), "question": user_input})
        print("Bot: ", result) 
    return result

# query = "How do I schedule an advising session?"
# response = answer_question(query)
# print(response)

if __name__ == "__main__":
    handle_conv()