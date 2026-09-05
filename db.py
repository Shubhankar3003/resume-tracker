import os
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Creates a local storage directory
os.makedirs("./resume_tracker_db", exist_ok=True)

# Initializes an embedded ChromaDB client pointing to local directory
client = chromadb.PersistentClient(path="./resume_tracker_db")

# Loads local sentence transformer for vector generation
embedding_fn = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2",
    normalize_embeddings=True
)

# Connects to create collection using cosine distance metric
collection = client.get_or_create_collection(
    name="resumes",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}
)