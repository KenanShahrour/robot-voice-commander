# Microspot Voice Commander

A local, edge-deployed voice interface designed for the **Microspot Mission Control System**. This project serves as a technical proof-of-concept for hands-free AI assistance in high-stakes field operations.

## ⚡ The Problem & Solution
Security officers and operators in the field (such as those driving M-patrol units) often cannot monitor complex dashboards while performing active tasks. 

**Microspot Voice Commander** provides a private, on-premise voice assistant that allows users to:
* Check real-time robot status without looking at a screen.
* Query PDF technical manuals via voice.
* Maintain operational focus while retrieving critical data.

## 🛠️ Technical Architecture
This system is architected for edge deployment (e.g., NVIDIA Orin), prioritizing low latency and privacy.

| Component | Tech Stack | Justification |
| :--- | :--- | :--- |
| **The Brain (LLM)** | **Llama-3.2 (3B)** | Optimized for edge units; fits in <4GB VRAM with high reasoning capability. |
| **Vector DB** | **Qdrant** | Production-grade server supporting **Hybrid Search** (keywords + vectors) for error codes. |
| **Voice I/O** | **Faster-Whisper** | CTranslate2 backend reduces STT inference time by 4x vs. standard Whisper. |
| **RAG Engine** | **Nomic Embeddings** | Supports 8k context window and outperforms larger models on local retrieval. |
| **Agent Logic** | **Deterministic Router** | A custom Python router for reliability instead of "black-box" agent frameworks. |
| **Infrastructure** | **Docker & Compose** | Ensures environment consistency between development and the robot's Linux OS. |

## 🚀 Key Features
* **Edge-Optimized:** Designed to run entirely on-premise with zero reliance on external APIs.
* **Hybrid RAG:** Combines semantic search with keyword matching to ensure technical manuals are indexed accurately.
* **Low Latency:** Uses a native TTS engine for near-instant responses.
* **Reliability:** Explicit intent routing ensures the system accurately distinguishes between live telemetry and static rules.

---
