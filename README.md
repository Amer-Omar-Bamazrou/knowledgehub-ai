# KnowledgeHub AI

KnowledgeHub AI is a production-oriented backend platform for building an AI-powered knowledge base.

The system allows users to upload documents, extract and process their content, generate vector embeddings, store them in PostgreSQL using `pgvector`, and ask questions against their personal knowledge base using Retrieval-Augmented Generation (RAG).

The project is being developed as part of a practical Generative AI engineering roadmap, with an emphasis on backend engineering, AI application architecture, security, testing, and production-oriented development.

---

## Overview

KnowledgeHub AI follows a complete document-to-answer pipeline:

```text
User Uploads TXT/PDF
        |
        v
Document Parser
(pypdf / UTF-8)
        |
        v
Text Chunking
(500 words / 50-word overlap)
        |
        v
Embeddings
(nomic-embed-text)
        |
        v
PostgreSQL + pgvector
(Vector Storage)
        |
        v
Semantic Search
(Cosine Similarity)
        |
        v
Relevant Document Chunks
        |
        v
RAG Context
        |
        v
Qwen3 4B via Ollama
        |
        v
AI Response
```

---

## Features

### Authentication

KnowledgeHub AI includes user authentication and authorization using:

- JWT access tokens
- OAuth2 password flow
- Argon2 password hashing
- Protected API endpoints
- User ownership of documents
- User-level document isolation

Users must authenticate before accessing protected resources.

### Document Management

Authenticated users can:

- Create documents through the API
- Retrieve their documents
- Retrieve individual documents
- Upload TXT files
- Upload PDF files
- Automatically extract text from uploaded documents
- Automatically chunk document content
- Generate embeddings for each chunk
- Store document chunks and embeddings in PostgreSQL

Currently supported file types:

- `.txt`
- `.pdf`

### PDF Processing

PDF documents are processed using `pypdf`.

The ingestion pipeline extracts text from each PDF page and combines the extracted content before storing and processing the document.

```text
PDF
 |
 v
pypdf
 |
 v
Extracted Text
 |
 v
Document
 |
 v
Text Chunks
 |
 v
Embeddings
```

---

## Retrieval-Augmented Generation

The core AI functionality is based on Retrieval-Augmented Generation (RAG).

Instead of sending a question directly to the language model, KnowledgeHub AI first searches the user's stored knowledge base for relevant information.

The retrieved document chunks are then provided to the language model as context.

```text
User Question
      |
      v
Question Embedding
      |
      v
Vector Similarity Search
      |
      v
Relevant Document Chunks
      |
      v
Context Construction
      |
      v
Qwen3 4B
      |
      v
Grounded Answer
```

This allows the system to answer questions using information retrieved from the user's knowledge base.

---

## Semantic Search

KnowledgeHub AI uses vector embeddings to perform semantic search.

### Embedding Model

```text
nomic-embed-text
```

Embeddings are generated locally through Ollama and stored in PostgreSQL using `pgvector`.

Current embedding dimension:

```text
768
```

The retrieval system uses vector similarity to identify document chunks that are most relevant to a user's question.

### Relevance Threshold

The retrieval system includes a relevance threshold to reduce retrieval of unrelated document chunks.

Current threshold:

```text
0.50
```

Retrieved chunks whose cosine distance exceeds the configured threshold are excluded from the RAG context.

---

## Local AI Models

KnowledgeHub AI currently uses Ollama for local AI inference.

### Generation Model

```text
qwen3:4b
```

### Embedding Model

```text
nomic-embed-text
```

The models run locally rather than relying on a hosted LLM API.

---

## Technology Stack

### Backend

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic

### Database

- PostgreSQL 17
- SQLAlchemy
- Alembic
- pgvector
- psycopg

### Authentication & Security

- JWT
- OAuth2
- PyJWT
- Argon2
- pwdlib

### Generative AI

- Ollama
- Qwen3 4B
- nomic-embed-text
- Embeddings
- Semantic Search
- Retrieval-Augmented Generation (RAG)

### Document Processing

- pypdf
- TXT processing
- Document chunking

### Infrastructure

- Docker
- Docker Compose

### Testing

- pytest
- RAG evaluation
- Retrieval testing
- Document parser testing

---

## Architecture

The application is organized into several layers:

```text
                    KnowledgeHub AI
                          |
        +-----------------+-----------------+
        |                 |                 |
        v                 v                 v
      API Layer       Service Layer     Database Layer
        |                 |                 |
        |                 |                 |
   FastAPI Routes    AI / RAG Services   PostgreSQL
   Authentication    Embeddings          pgvector
   Documents         Retrieval
   AI                Chunking
                     Parsing
```

The main application flow is:

```text
Client
  |
  v
FastAPI
  |
  +--------------------+
  |                    |
  v                    v
Authentication      Document API
  |                    |
  v                    v
JWT / User         Document Storage
Ownership               |
                        v
                 Chunking + Embeddings
                        |
                        v
                  PostgreSQL/pgvector
                        |
                        v
                    RAG Pipeline
                        |
                        v
                   Ollama / Qwen3
```

---

## Project Structure

```text
knowledgehub-ai/
|
+-- app/
|   |
|   +-- api/
|   |   +-- auth.py
|   |   +-- dependencies.py
|   |   +-- documents.py
|   |   +-- ai.py
|   |
|   +-- core/
|   |   +-- config.py
|   |   +-- security.py
|   |
|   +-- db/
|   |   +-- database.py
|   |
|   +-- models/
|   |   +-- user.py
|   |   +-- document.py
|   |   +-- document_chunk.py
|   |
|   +-- schemas/
|   |   +-- user.py
|   |   +-- document.py
|   |   +-- ai.py
|   |
|   +-- services/
|   |   +-- ai_service.py
|   |   +-- embedding_service.py
|   |   +-- chunking_service.py
|   |   +-- document_parser.py
|   |   +-- retrieval_service.py
|   |   +-- knowledge_service.py
|   |
|   +-- main.py
|
+-- alembic/
|   +-- versions/
|
+-- scripts/
|   +-- evaluate_rag.py
|
+-- tests/
|   +-- test_document_parser.py
|   +-- test_document_parser_pdf.py
|   +-- test_rag_evaluation.py
|   +-- test_retrieval_threshold.py
|
+-- .env
+-- .gitignore
+-- alembic.ini
+-- docker-compose.yml
+-- Dockerfile
+-- requirements.txt
+-- README.md
```

---

## API

The application exposes a REST API through FastAPI.

### Authentication

#### Register

```http
POST /auth/register
```

Creates a new user account.

#### Login

```http
POST /auth/login
```

Authenticates a user and returns a JWT access token.

---

### Documents

#### Create Document

```http
POST /documents/
```

Creates a document from JSON input.

#### List Documents

```http
GET /documents/
```

Returns documents belonging to the authenticated user.

#### Get Document

```http
GET /documents/{document_id}
```

Returns a specific document belonging to the authenticated user.

#### Upload Document

```http
POST /documents/upload
```

Uploads and processes a TXT or PDF document.

The upload pipeline automatically:

1. Validates the file type
2. Reads the file
3. Extracts the text
4. Creates the document
5. Splits the document into chunks
6. Generates embeddings
7. Stores the chunks and embeddings
8. Associates the document with the authenticated user

---

### AI

#### Generate AI Response

```http
POST /ai/generate
```

Sends a prompt directly to the local language model.

#### Ask Knowledge Base

```http
POST /ai/ask
```

Uses the complete RAG pipeline:

```text
Question
   |
   v
Embedding
   |
   v
Vector Search
   |
   v
Relevant Chunks
   |
   v
Context
   |
   v
Qwen3
   |
   v
Answer
```

---

## Database Architecture

KnowledgeHub AI uses PostgreSQL as its primary database.

The main database entities are:

```text
users
documents
document_chunks
```

Relationships:

```text
User
 |
 +----< Documents
           |
           +----< Document Chunks
```

Each document belongs to a user.

Each document can contain multiple chunks.

Each chunk can contain a vector embedding.

---

## Database Migrations

Database schema changes are managed using Alembic.

### Apply migrations

```bash
alembic upgrade head
```

### Check current migration

```bash
alembic current
```

### Check for schema differences

```bash
alembic check
```

### Create a migration

```bash
alembic revision --autogenerate -m "description"
```

---

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Amer-Omar-Bamazrou/knowledgehub-ai.git
cd knowledgehub-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL

The project includes Docker configuration for PostgreSQL.

```bash
docker compose up -d
```

Check the running containers:

```bash
docker ps
```

### 5. Run Database Migrations

```bash
alembic upgrade head
```

### 6. Start Ollama

Make sure Ollama is installed and running.

The project currently expects:

```text
qwen3:4b
```

and:

```text
nomic-embed-text
```

Pull the models if necessary:

```bash
ollama pull qwen3:4b
ollama pull nomic-embed-text
```

### 7. Start FastAPI

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger can be used to test:

- Authentication
- Document creation
- Document uploads
- AI generation
- RAG queries

---

## Testing

The project uses `pytest`.

Run the complete test suite:

```bash
pytest
```

The test suite covers:

- TXT document parsing
- PDF document parsing
- Retrieval relevance
- RAG evaluation
- Unknown-question handling

Current test result:

```text
6 passed
```

---

## RAG Evaluation

KnowledgeHub AI includes an evaluation script for testing the RAG pipeline.

Run:

```bash
python -m scripts.evaluate_rag
```

Example evaluation:

```text
PASS: What framework is used to build the API?
PASS: What database system is used?
PASS: What is SQLAlchemy used for?
PASS: Who is the president of the United States?

RAG Evaluation
--------------
Total cases: 4
Passed: 4
Failed: 0
Retrieval accuracy: 100.0%
```

The evaluation provides a repeatable way to check RAG behaviour as the system evolves.

---

## Example RAG Workflow

Suppose a user uploads a document containing:

```text
FastAPI is a Python web framework used to build modern APIs.

PostgreSQL is a relational database used to store application data.

SQLAlchemy is a Python ORM used to interact with relational databases.
```

The document is processed into chunks and embedded.

The user can then ask:

```text
What framework is used to build the API?
```

KnowledgeHub AI performs semantic retrieval and passes the relevant document context to Qwen3.

The resulting answer can be:

```text
FastAPI
```

The key concept is that the model receives relevant information retrieved from the user's knowledge base as context.

---

## Security

The project currently includes:

- Password hashing with Argon2
- JWT-based authentication
- OAuth2 password authentication
- Protected API routes
- User-specific document ownership
- User-level retrieval isolation
- Relevance filtering before RAG generation

Sensitive configuration is stored through environment variables rather than being hard-coded into application logic.

---

## Current Development Status

KnowledgeHub AI has completed the core backend, database, authentication, document ingestion, semantic search, and RAG implementation stages.

### Backend Foundation

- [x] FastAPI application
- [x] REST API
- [x] Application structure
- [x] Configuration management

### Database

- [x] PostgreSQL
- [x] SQLAlchemy
- [x] Alembic
- [x] Database migrations
- [x] pgvector
- [x] Document chunks
- [x] Vector embeddings

### Authentication

- [x] User registration
- [x] Password hashing
- [x] JWT authentication
- [x] OAuth2 login
- [x] Protected routes
- [x] User document ownership
- [x] User isolation

### Document Intelligence

- [x] TXT ingestion
- [x] PDF ingestion
- [x] PDF text extraction
- [x] Document chunking
- [x] Embedding generation
- [x] Vector storage

### RAG

- [x] Question embeddings
- [x] Semantic retrieval
- [x] Cosine similarity
- [x] Relevance threshold
- [x] Context construction
- [x] LLM generation
- [x] Knowledge-base question answering
- [x] RAG evaluation

### Testing

- [x] Unit tests
- [x] PDF parser tests
- [x] Retrieval tests
- [x] RAG evaluation
- [x] Unknown-question testing

---

## Roadmap

The project will continue toward a more production-oriented Generative AI architecture.

### Phase 1 — Backend Foundation

- [x] FastAPI
- [x] Python
- [x] REST API
- [x] Project architecture

### Phase 2 — Database

- [x] PostgreSQL
- [x] SQLAlchemy
- [x] Alembic
- [x] pgvector

### Phase 3 — Authentication

- [x] User registration
- [x] JWT authentication
- [x] Password hashing
- [x] Protected endpoints
- [x] User isolation

### Phase 4 — Document Processing

- [x] TXT ingestion
- [x] PDF ingestion
- [x] Text extraction
- [x] Chunking

### Phase 5 — Semantic Search

- [x] Embeddings
- [x] Vector storage
- [x] Similarity search
- [x] Relevance threshold

### Phase 6 — RAG

- [x] Retrieval pipeline
- [x] Context construction
- [x] LLM generation
- [x] Knowledge-base Q&A
- [x] RAG evaluation

### Phase 7 — Production Hardening

- [ ] Improved API error handling
- [ ] Structured logging
- [ ] Improved configuration management
- [ ] Rate limiting
- [ ] Improved document validation
- [ ] More comprehensive integration tests
- [ ] CI/CD
- [ ] Production deployment

### Phase 8 — Advanced RAG

- [ ] Improved chunking strategies
- [ ] Metadata filtering
- [ ] Hybrid search
- [ ] Reranking
- [ ] Improved source citations
- [ ] RAG evaluation datasets
- [ ] Retrieval metrics

### Phase 9 — AI Agents

- [ ] LangGraph
- [ ] Tool calling
- [ ] Agent workflows
- [ ] Guardrails
- [ ] Agent evaluation
- [ ] Multi-step reasoning workflows

---

## Engineering Goals

### Backend Engineering

Build strong practical experience in:

- API design
- Database architecture
- Authentication
- ORM usage
- Database migrations
- Testing
- Docker
- Production deployment

### Generative AI Engineering

Develop practical experience with:

- LLM integration
- Local inference
- Embeddings
- Vector databases
- Semantic search
- RAG
- Evaluation
- AI application architecture
- Agent workflows

### Production Engineering

The long-term goal is to move the project beyond a simple AI prototype toward a maintainable production-oriented system.

---

## Development Philosophy

KnowledgeHub AI follows a practical engineering approach:

```text
Learn
  |
  v
Build
  |
  v
Test
  |
  v
Evaluate
  |
  v
Improve
  |
  v
Deploy
```

The focus is on understanding how the individual components work together rather than simply integrating AI APIs into an application.

---

## Author

**Amer Omar Bamazrou**

Software Engineering Graduate  
First Class Honours — De Montfort University

### GitHub

https://github.com/Amer-Omar-Bamazrou

### Project

https://github.com/Amer-Omar-Bamazrou/knowledgehub-ai
