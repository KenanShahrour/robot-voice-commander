import qdrant_client
from qdrant_client import QdrantClient
from langchain_community.embeddings import OllamaEmbeddings

# Initialize
client = QdrantClient(url="http://localhost:6333")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

query = "What happens if battery is low?"
print(f"\nQuerying: {query}")

# Embed the query (Turn text into numbers)
query_vector = embeddings.embed_query(query)

# perform search
try:
    results = client.query_points(
        collection_name="micropolis_manuals",
        query=query_vector, 
        limit=1,
        with_payload=True # need the text back, not just the ID
    )
    
    # query_points returns a generic object, the list is usually in .points
    hits = results.points

    for hit in hits:
        print(f"\nFOUND MATCH (Score: {hit.score:.4f}):")
        
        payload = hit.payload
        content = payload.get('page_content', 'No Content Found')
        print(f"--> {content}")
        
        # Search analysis based on score
        if hit.score > 0.5:
            print("   [ANALYSIS]: High confidence match. Good context.")
        else:
            print("   [ANALYSIS]: Low confidence. The AI might hallucinate.")

except Exception as e:
    print(f"\n SEARCH FAILED: {e}")