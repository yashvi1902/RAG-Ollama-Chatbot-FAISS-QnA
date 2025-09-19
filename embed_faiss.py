import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# Step 1: Load the JSON data
with open('clean_data_all.json', 'r') as f:
    data = json.load(f)

# Step 2: Flatten the tokenized data
# Assuming each 'content' in your data is a list of strings
tokenized_data = []
for item in data:
    for section in item['sections']:
        for content_list in section['content']:
            tokenized_data.extend(content_list)  # Flatten the content lists

# Step 3: Convert tokenized data to Document objects
documents = [Document(page_content=text) for text in tokenized_data]
print("Converting tokenized data to Document objects")

# Step 4: Initialize HuggingFace embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Initializing HuggingFace embeddings")

# Step 5: Create the FAISS index
print("Creating the FAISS index")
faiss_index = FAISS.from_documents(documents, embedding_model)

# Step 6: Save the FAISS index locally
faiss_index.save_local("faiss_index")

print("FAISS index created and saved locally.")

# # Perform similarity search
queries = [
    "Arboretum at Cal State Fullerton",
    "how many programs are offered by CSUF?",
    "MS Computer science graduate advisor contact details",
    "How many credits can be transfer credits?",
    "how can i check my Scholarship eligibility?"
]

# Iterate over queries and output search results
for query in queries:
    query_embedding = embedding_model.embed_query(query)  # Explicitly embed the query
    docs = faiss_index.similarity_search_by_vector(query_embedding)  # Perform vector-based search

    print(f"Query: {query}")
    for doc in docs:
        print(doc.page_content)
    print("\n\n")
    




