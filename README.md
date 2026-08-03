# Adaptive RAG with ChromaDB

An adaptive Retrieval-Augmented Generation (RAG) system that intelligently routes queries to the appropriate knowledge source using LangGraph and ChromaDB for vector storage.

## Features

- **Adaptive Query Routing**: Automatically classifies queries to route to document retrieval, general knowledge, or web search
- **ChromaDB Vector Storage**: Persistent vector embeddings using ChromaDB
- **In-Memory Chat History**: Session-based conversation history without external database dependencies
- **Document Upload**: Support for PDF and TXT files with automatic chunking and embedding
- **ReAct Agent**: Tool-using agent for document retrieval
- **Answer Verification**: Faithfulness checking for generated answers

## Architecture

The system uses a LangGraph-based workflow with the following nodes:

1. **Query Analysis** - Classifies incoming queries (index/general/search)
2. **Retriever** - Uses ReAct agent to search document store
3. **Grade** - Evaluates retrieval relevance
4. **Rewrite** - Reformulates queries for better retrieval
5. **Generate** - Produces final answers
6. **Web Search** - Fallback for real-time information
7. **General LLM** - Handles casual conversation and common knowledge

## Requirements

- Python 3.10+
- Groq API key (for LLM)
- Tavily API key (for web search)

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Create a `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=adaptive_rag_documents
```

## Usage

### Start the API Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

- **POST /rag/query** - Query the RAG system
  ```json
  {
    "query": "Your question here"
  }
  ```

- **POST /rag/documents/upload** - Upload a document
  - File: PDF or TXT (multipart/form-data)
  - Header: `X-Description: Your document description`

### Run Streamlit UI

```bash
streamlit run streamlit_app/main.py
```

## Project Structure

```
Adaptive_RAG/
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── src/
│   ├── main.py              # FastAPI entry point
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── config/
│   │   ├── settings.py      # Configuration management
│   │   └── prompts.yaml     # Prompt templates
│   ├── core/
│   │   ├── config.py        # Logging setup
│   │   └── logger.py        # Logger instance
│   ├── llms/
│   │   ├── groq.py          # Groq LLM configuration
│   │   └── openai.py        # OpenAI LLM configuration
│   ├── memory/
│   │   └── chathistory_in_memory.py  # In-memory chat history
│   ├── models/
│   │   ├── state.py         # LangGraph state schema
│   │   ├── grade.py         # Document grading model
│   │   ├── route_identifier.py  # Query classification model
│   │   ├── query_request.py # API request model
│   │   └── verification_result.py  # Answer verification model
│   ├── rag/
│   │   ├── graph_builder.py # LangGraph workflow
│   │   ├── retriever_setup.py # ChromaDB retriever
│   │   ├── reAct_agent.py   # ReAct agent for retrieval
│   │   └── document_upload.py  # Document processing
│   └── tools/
│       ├── graph_tools.py   # Graph routing tools
│       └── common_tools.py  # Utility functions
└── streamlit_app/
    └── main.py              # Streamlit UI
```

## How It Works

1. **Document Upload**: Documents are chunked, embedded with HuggingFace embeddings, and stored in ChromaDB
2. **Query Classification**: Incoming queries are classified as:
   - `index`: Answerable from uploaded documents
   - `general`: Answerable from common knowledge
   - `search`: Requires real-time/web information
3. **Adaptive Routing**: Based on classification, queries route to appropriate handler
4. **Retrieval & Grading**: Document queries use ReAct agent; results are graded for relevance
5. **Answer Generation**: Final answers are generated and verified for faithfulness

## License

MIT