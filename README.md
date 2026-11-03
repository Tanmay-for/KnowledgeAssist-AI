# KnowledgeAssist AI

### A Local RAG-Based and Knowledge Graph-Enhanced AI Chatbot

KnowledgeAssist AI is an intelligent educational chatbot designed to help students understand academic subjects using their own study materials.

The system combines **Retrieval-Augmented Generation (RAG), Knowledge Graphs, and Prompt Engineering** to provide context-aware answers from uploaded PDF and TXT documents.

It uses locally running AI models through Ollama, ChromaDB for vector storage, and NetworkX for knowledge graph management.

---

## 1. Project Objectives

- Provide an intelligent chatbot for academic learning.
- Allow students to upload their own study materials.
- Retrieve relevant information from uploaded documents.
- Represent concepts and their relationships using a Knowledge Graph.
- Generate structured answers using prompt engineering.
- Run the entire application locally without paid AI APIs.

## 2. Key Features

- **Document Upload:** Upload PDF and TXT study materials.
- **RAG-Based Question Answering:** Retrieve relevant document chunks using semantic similarity.
- **Knowledge Graph:** Extract concepts and relationships and display them as an interconnected graph.
- **Prompt Engineering:** Support different response styles, including Simple, Exam, Lab, Viva, and Detailed modes.
- **Local LLM:** Generate responses using Ollama.
- **Vector Database:** Store document embeddings using persistent ChromaDB.
- **Document Management:** View, upload, and delete documents.
- **Interactive Graph Visualization:** Explore concepts, relationships, and directed connections.
- **Source References:** Display document names and page references in chatbot answers.
- **Local Storage:** Keep uploaded materials, embeddings, and graph data on the local machine.

## 3. Technologies Used

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Backend development            |
| FastAPI               | Backend API framework          |
| React.js              | Frontend development           |
| Vite                  | Frontend development server    |
| Ollama                | Local LLM and embedding models |
| Qwen 2.5:3B           | Response generation            |
| Nomic Embed Text      | Text embeddings                |
| ChromaDB              | Vector database                |
| NetworkX              | Knowledge Graph creation       |
| React Force Graph 2D  | Graph visualization            |
| PyMuPDF               | PDF text extraction            |
| HTML, CSS, JavaScript | Frontend interface             |

## 4. System Architecture

The application follows this workflow:

```text
                 USER
                   |
                   v
          React Frontend
                   |
                   v
             FastAPI
                   |
          +--------+--------+
          |                 |
          v                 v
     DOCUMENT UPLOAD     USER QUESTION
          |                 |
          v                 v
     Text Extraction    Query Embedding
          |                 |
          v                 v
       Chunking         ChromaDB Search
          |                 |
          v                 v
     Ollama Embeddings  Relevant Chunks
          |
          v
       ChromaDB

     Document Text
          |
          v
    Concept Extraction
          |
          v
    NetworkX Knowledge
          Graph

     Relevant Chunks
          +
    Graph Relationships
          +
    Prompt Template
          |
          v
       Ollama LLM
          |
          v
     Generated Answer
          |
          v
     React Frontend
```

## 5. Project Structure

```text
KnowledgeAssist-AI/
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── upload.py
│       │   ├── chat.py
│       │   ├── graph.py
│       │   └── documents.py
│       │
│       ├── core/
│       │   └── config.py
│       │
│       ├── graph/
│       │   ├── knowledge_graph.py
│       │   └── graph_extraction.py
│       │
│       ├── prompts/
│       │   └── templates.py
│       │
│       ├── rag/
│       │   ├── vector_store.py
│       │   ├── retriever.py
│       │   └── rag_pipeline.py
│       │
│       ├── services/
│       │   ├── document_service.py
│       │   ├── chunking_service.py
│       │   ├── embedding_service.py
│       │   ├── llm_service.py
│       │   └── document_registry.py
│       │
│       └── main.py
│
├── data/
│   ├── chroma_db/
│   ├── knowledge_graph/
│   ├── uploads/
│   │   ├── permanent/
│   │   └── temporary/
│   └── documents.json
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   ├── package.json
│   └── index.html
│
├── .env
├── .gitignore
├── requirements.txt
├── rebuild_knowledge_graph.py
├── connect_graph_root.py
└── README.md
```

## 6. Prerequisites

Install the following software before running the project:

1. Python 3.12 recommended.
2. Node.js and npm.
3. Ollama.
4. Visual Studio Code.
5. Git (for version control and GitHub upload).

### Download Links

- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Ollama: https://ollama.com/download
- VS Code: https://code.visualstudio.com/
- Git: https://git-scm.com/downloads

## 7. Ollama Model Setup

Install Ollama and open PowerShell or the VS Code terminal.

Download the required models:

```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

The project uses:

- `qwen2.5:3b` for generating chatbot responses.
- `nomic-embed-text` for generating document and query embeddings.

Check installed models:

```bash
ollama list
```

Ensure Ollama is running before starting the chatbot.

## 8. Backend Installation

Open the project folder in VS Code.

Open a terminal in the main project directory.

### Step 1: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 2: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Python dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Start the backend

```powershell
python -m uvicorn backend.app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## 9. Frontend Installation

Open a second terminal in VS Code.

Navigate to the frontend directory:

```powershell
cd frontend
```

Install the frontend dependencies:

```powershell
npm install
```

Start the frontend development server:

```powershell
npm run dev
```

Open the local URL displayed in the terminal, usually:

http://localhost:5173

## 10. Environment Configuration

Create a `.env` file in the main project directory.

Configure it as follows:

```env
APP_NAME=KnowledgeAssist AI

OLLAMA_BASE_URL=http://localhost:11434

LLM_MODEL=qwen2.5:3b
EMBEDDING_MODEL=nomic-embed-text

CHROMA_DB_PATH=./data/chroma_db
KNOWLEDGE_GRAPH_PATH=./data/knowledge_graph

UPLOAD_TEMP_PATH=./data/uploads/temporary
UPLOAD_PERMANENT_PATH=./data/uploads/permanent
```

Do not upload your private `.env` file to GitHub.

## 11. How the Project Works

### A. Document Upload

Users upload PDF or TXT documents through the frontend.

The backend extracts document text, divides it into chunks, and generates embeddings using Ollama.

### B. RAG Pipeline

When a student asks a question:

1. The question is converted into an embedding.
2. ChromaDB retrieves the most relevant document chunks.
3. Retrieved text is passed to the LLM as context.
4. The LLM generates an answer based on the retrieved information.
5. The application displays the response and available document sources.

### C. Knowledge Graph

The Knowledge Graph represents academic concepts as nodes and their relationships as directed edges.

NetworkX manages the graph, and React Force Graph 2D displays the connections visually.

For the current OOP implementation, concepts include:

- Class
- Object
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Constructor
- Destructor
- Function
- Data Member
- Member Function

### D. Prompt Engineering

Prompt templates control how the chatbot generates answers.

Different response modes help students obtain answers in different formats:

- Simple: Easy-to-understand explanations.
- Exam: Structured examination-style answers.
- Lab: Practical and programming-focused answers.
- Viva: Short question-and-answer explanations.
- Detailed: In-depth explanations with examples.

## 12. Supported File Types

| Property          | Supported               |
| ----------------- | ----------------------- |
| PDF documents     | Yes                     |
| TXT documents     | Yes                     |
| Maximum file size | 20 MB                   |
| PDF OCR           | Not currently supported |
| Permanent storage | Yes                     |
| Temporary storage | Yes                     |

Scanned PDFs that do not contain extractable text may not be processed correctly.

## 13. Testing the Application

Use the following questions to test the chatbot:

**Test 1: RAG Testing**

```text
Explain the four main principles of Object-Oriented Programming.
```

Check whether the answer is based on your uploaded documents and includes source references.

**Test 2: Knowledge Graph Testing**

```text
Explain the relationship between Polymorphism and Function.
```

Check whether the chatbot retrieves the actual graph relationship.

**Test 3: Graph Path Testing**

```text
Show the relationship path from Object-Oriented Programming
to Implementation Details.
```

Expected path:

```text
Object-Oriented Programming
          |
       includes
          |
      Abstraction
          |
        hides
          |
Implementation Details
```

**Test 4: Prompt Engineering Testing**

Ask the same question using Simple, Exam, Viva, and Detailed modes.

Check whether the response format changes according to the selected mode.

## 14. Data Storage

The project stores its data locally.

| Data                | Storage Location                            |
| ------------------- | ------------------------------------------- |
| Vector embeddings   | `data/chroma_db/`                           |
| Knowledge Graph     | `data/knowledge_graph/knowledge_graph.json` |
| Permanent documents | `data/uploads/permanent/`                   |
| Temporary documents | `data/uploads/temporary/`                   |
| Document registry   | `data/documents.json`                       |

The local model does not need to be retrained when new documents are uploaded. Instead, the document embeddings and Knowledge Graph are updated through the ingestion process.

## 15. Limitations

- Knowledge Graph extraction currently uses predefined OOP concepts and rule-based relationship patterns.
- New types of concepts may require updates to the extraction rules.
- Graph relationships are not guaranteed to be inferred correctly from every sentence.
- Scanned PDFs require OCR support, which is not currently implemented.
- LLM-generated responses can occasionally contain inaccurate information.
- Performance depends on the available system hardware and local model size.

## 16. Future Enhancements

- Support for additional academic subjects.
- Improved automatic concept and relationship extraction.
- Dynamic knowledge graph expansion.
- Advanced PDF processing and OCR.
- More accurate source-level answer verification.
- Chat history and conversation management.
- Export answers as PDF.
- Improved graph filtering and concept exploration.

## 17. License

This project is developed for academic and educational purposes.

---

## 18. Author

**Project Name:** KnowledgeAssist AI

**Project Type:** Prompt Engineering / AI-Based Educational Chatbot

**Core Technologies:** RAG, Knowledge Graph, Prompt Engineering, ChromaDB, NetworkX, FastAPI, React, and Ollama.
