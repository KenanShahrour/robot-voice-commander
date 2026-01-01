# brain that decides what to do
# implements Router Logic. choosing between RAG (history) and tools (mock live data)
import ollama
from qdrant_client import QdrantClient
from langchain_community.embeddings import OllamaEmbeddings
from src.tools import get_fleet_status, dispatch_unit

LLM_MODEL = "llama3.2"  # Fast and Edge Optimized (assuming working with nvidia orin hardware and also for my limited laptop capabilities)
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "micropolis_manuals"

class MicrospotAgent:
    def __init__(self):
        print("[INIT] Connecting to Memory (Qdrant)...")
        self.client = QdrantClient(url=QDRANT_URL)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # prompt defines the personality and rules
        self.system_prompt = (
            "You are the Voice Command Interface for Micropolis Security. "
            "You have access to two data sources:\n"
            "1. LIVE FLEET DATA: For questions about specific robot status/location.\n"
            "2. PROTOCOLS (RAG): For questions about rules, errors, or maintenance.\n\n"
            "RULES:\n"
            "- Be brief and professional (Military style).\n"
            "- If the user asks about a specific Unit (Alpha/Beta), use the Live Data.\n"
            "- If the user asks 'How to' or 'What is', use the Protocol RAG.\n"
        )

    def retrieve_protocol(self, query):
        """Performs the Vector Search (RAG)"""
        print(f"   [RAG SEARCH] Looking up protocols for: '{query}'...")
        query_vector = self.embeddings.embed_query(query)
        
        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=1,
            with_payload=True
        )
        
        if results.points and results.points[0].score > 0.45:
            return results.points[0].payload['page_content']
        return None

    def ask(self, user_text):
        print(f"\n[USER]: {user_text}")
        
        context = ""
        
        # router logic (the brain)
        # heck for specific Robot Names (Intent: Live Data)
        if "alpha" in user_text.lower():
            print("   [ROUTER] Detected Intent: Live Fleet Data")
            data = get_fleet_status("alpha")
            context += f"\nLIVE_TELEMETRY: {data}\n"
            
        elif "beta" in user_text.lower():
            print("   [ROUTER] Detected Intent: Live Fleet Data")
            data = get_fleet_status("beta")
            context += f"\nLIVE_TELEMETRY: {data}\n"

        # if no robot name, or if it looks like a "How to" question, check RAG
        else:
            print("   [ROUTER] Detected Intent: Protocol Search")
            rag_data = self.retrieve_protocol(user_text)
            if rag_data:
                context += f"\nPROTOCOL_MANUAL: {rag_data}\n"
        
        # GENERATION
        # Combine the System Prompt + The Retrieved Data + The User Question
        full_prompt = f"{self.system_prompt}\n\nCONTEXT DATA:\n{context}\n\nUSER QUESTION: {user_text}"
        
        print("   [LLM] Generating Response...")
        # Stream the response for that "Real-Time" feel
        stream = ollama.chat(
            model=LLM_MODEL,
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=True
        )
        
        full_reply = ""
        print("[AI]: ", end="")
        for chunk in stream:
            token = chunk['message']['content']
            print(token, end="", flush=True)
            full_reply += token
        print("\n")
        return full_reply

# SIMPLE TESTING LOOP
if __name__ == "__main__":
    agent = MicrospotAgent()
    
    # # Test 1: RAG Question
    # agent.ask("What do I do if the battery is critically low?")
    
    # # Test 2: Live Data Question
    # agent.ask("What is the status of Unit Alpha?")