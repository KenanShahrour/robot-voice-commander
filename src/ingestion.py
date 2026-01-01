import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

DATA_PATH = "./data/protocols/security_manual.txt"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "micropolis_manuals"

def ingest_docs():
    print("[LOADING] Reading the manual...")
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: File not found at {DATA_PATH}")
        return
    
    loader = TextLoader(DATA_PATH)
    documents = loader.load()
    print(f"   Loaded {len(documents)} document(s).")

    print("[CHUNKING] Splitting text into digestible pieces...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(documents)
    print(f"   Created {len(splits)} chunks.")

    print("[EMBEDDING] initializing models...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Measure the vector size dynamically
    test_embedding = embeddings.embed_query("test")
    vector_size = len(test_embedding)
    print(f"   Detected Vector Size: {vector_size}")

    print("[DATABASE] Resetting Qdrant Collection...")
    # Initialize the client explicitly (No gRPC to avoid port errors)
    client = QdrantClient(url=QDRANT_URL, prefer_grpc=False)
    
    # Check if collection exists and delete it (Start Fresh)
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
    
    # Create the collection explicitly
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

    print("[INSERTING] Pushing vectors to DB...")
    # Now we pass the READY client to LangChain
    vector_store = Qdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings,
    )
    
    vector_store.add_documents(splits)
    print("SUCCESS: Knowledge Base Updated!")

if __name__ == "__main__":
    ingest_docs()