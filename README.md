# [cite_start]Microspot Voice Commander [cite: 2]

**Repository Description:** A privacy-first, edge-deployed AI voice assistant designed for hands-free mission control and field operations.

---

### ⚡ Overview
[cite_start]I architected this solution [cite: 3] [cite_start]as a local, edge-deployed voice interface for the "Microspot" mission control system[cite: 4]. [cite_start]It serves as a proof of abilities for high-stakes environments where security officers cannot monitor complex dashboards while operating equipment[cite: 5]. 

[cite_start]This AI assistant is private (runs on-prem) and distinguishes between live data and static rules[cite: 6].

### 🛠️ Technical Architecture
[cite_start]This prototype was built to meet specific high-performance requirements for edge computing, such as NVIDIA Orin units[cite: 8].

| Component | Tech Stack | Justification (Why this tool?) |
| :--- | :--- | :--- |
| **Brain (LLM)** | **Llama-3.2 (3B)** | [cite_start]Optimized for edge devices; fits in <4GB VRAM while retaining strong reasoning[cite: 8]. |
| **Vector DB** | **Qdrant** | [cite_start]A production-grade server supporting Hybrid Search for specific error codes[cite: 8]. |
| **Voice I/O** | **Faster-Whisper (STT)** | [cite_start]Uses CTranslate2 backend to reduce inference time by 4x compared to standard Whisper[cite: 8]. |
| **RAG Engine** | **Nomic Embeddings** | [cite_start]Supports 8k context window and outperforms older models on local retrieval benchmarks[cite: 8]. |
| **Agent Logic** | **Python Router** | [cite_start]A deterministic router ensuring reliability by explicitly checking intent between Tools and RAG[cite: 8]. |
| **Infrastructure**| **Docker & Compose** | [cite_start]Ensures environment consistency between development and the robot's Linux OS[cite: 8]. |

### 🚀 Key Solutions
* [cite_start]**Hands-Free Operation:** Solves the problem for officers who cannot look at dashboards while driving M-patrol units[cite: 5].
* [cite_start]**Instant Information:** Allows users to quickly check robot status or read PDF manuals via voice[cite: 5].
* [cite_start]**Low Latency:** Utilizes native OS engines (pyttsx3) for zero-latency response in the field[cite: 8].
* [cite_start]**Privacy-First:** Designed to run entirely on-premise for secure mission control contexts[cite: 6].

---
