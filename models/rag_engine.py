from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load policies
with open("data/policies.txt", "r") as f:
    policies = f.readlines()

# Generate embeddings
policy_embeddings = model.encode(policies)

# Convert to numpy array
policy_embeddings = np.array(policy_embeddings)

# Create FAISS index
index = faiss.IndexFlatL2(policy_embeddings.shape[1])

# Add embeddings to index
index.add(policy_embeddings)

def retrieve_policy(query):

    # Convert query into embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding)

    # Search most similar policy
    distances, indices = index.search(query_embedding, k=1)

    return policies[indices[0][0]]
