# KnowledgeHub AI

KnowledgeHub AI is a production-oriented backend platform for building an AI-powered knowledge base.

The system allows users to upload documents, extract and process their content, generate vector embeddings, store them in PostgreSQL using `pgvector`, and ask questions against their personal knowledge base using Retrieval-Augmented Generation (RAG).

The project is being developed as part of a practical Generative AI engineering roadmap, with an emphasis on backend engineering, AI application architecture, security, testing, and production-oriented development.

---

## Overview

KnowledgeHub AI follows a complete document-to-answer pipeline:

```text
                ┌──────────────────────┐
                │      User Uploads    │
                │      TXT / PDF       │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Document Parser    │
                │   pypdf / UTF-8      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     Text Chunking    │
                │  500 words / overlap │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     Embeddings       │
                │  nomic-embed-text    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ PostgreSQL + pgvector│
                │   Vector Storage     │
                └──────────┬───────────┘
                           │
                           │ Semantic Search
                           ▼
                ┌──────────────────────┐
                │ Retrieval Service    │
                │ Cosine Similarity    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    RAG Context       │
                │ Relevant Chunks      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │      Qwen3 4B        │
                │       Ollama         │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     AI Response      │
                └──────────────────────┘
Features
Authentication

KnowledgeHub AI includes user authentication and authorization using:

JWT access tokens
OAuth2 password flow
Argon2 password hashing
Protected API endpoints
User ownership of documents
User-level document isolation

Users can register and authenticate before accessing protected resources.

Document Management

Authenticated users can:

Create documents through the API
Retrieve their documents
Retrieve individual documents
Upload TXT files
Upload PDF files
Automatically extract text from uploaded documents
Automatically chunk document content
Generate embeddings for each chunk

Currently supported file types:

.txt
.pdf
PDF Processing

PDF documents are processed using pypdf.

The ingestion pipeline extracts text from each PDF page and combines the extracted content before storing and processing the document.

PDF
 │
 ▼
pypdf
 │
 ▼
Extracted Text
 │
 ▼
Document
 │
 ▼
Chunks
Retrieval-Augmented Generation

The core AI functionality is based on Retrieval-Augmented Generation (RAG).

Instead of sending a question directly to the language model, KnowledgeHub AI first searches the user's stored knowledge base for relevant information.

The retrieved document chunks are then provided to the language model as context.

User Question
      │
      ▼
Question Embedding
      │
      ▼
Vector Similarity Search
      │
      ▼
Relevant Document Chunks
      │
      ▼
Context Construction
      │
      ▼
Qwen3
      │
      ▼
Grounded Answer

This allows the system to answer questions based on the documents stored in the user's knowledge base.

Semantic Search

KnowledgeHub AI uses vector embeddings to perform semantic search.

The current embedding model is:

nomic-embed-text

Embeddings are generated locally through Ollama and stored in PostgreSQL using pgvector.

The current embedding dimension is:

768

The retrieval system uses vector similarity to identify the document chunks most relevant to a user's question.

Relevance Threshold

The retrieval system includes a relevance threshold to reduce retrieval of unrelated document chunks.

Current threshold:

0.50

Retrieved chunks whose cosine distance exceeds the configured threshold are excluded from the RAG context.

This provides an additional layer of protection against irrelevant context being passed to the language model.

Local AI Models

KnowledgeHub AI currently uses Ollama for local AI inference.

Generation Model
qwen3:4b
Embedding Model
nomic-embed-text

The models run locally rather than relying on a hosted LLM API.

This allows development and experimentation with AI functionality without requiring a paid external inference API.

Technology Stack
Backend
Python 3.13
FastAPI
Uvicorn
Pydantic
Database
PostgreSQL 17
SQLAlchemy
Alembic
pgvector
psycopg
Authentication & Security
JWT
OAuth2
PyJWT
Argon2
pwdlib
AI / Machine Learning
Ollama
Qwen3 4B
nomic-embed-text
Embeddings
Semantic Search
Retrieval-Augmented Generation (RAG)
Document Processing
pypdf
TXT processing
Document chunking
Infrastructure
Docker
Docker Compose
Testing
pytest
RAG evaluation
Retrieval testing
Document parser testing
Project Structure
knowledgehub-ai/
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── dependencies.py
│   │   ├── documents.py
│   │   └── ai.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── document.py
│   │   └── document_chunk.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── document.py
│   │   └── ai.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── embedding_service.py
│   │   ├── chunking_service.py
│   │   ├── document_parser.py
│   │   ├── retrieval_service.py
│   │   └── knowledge_service.py
│   │
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── scripts/
│   └── evaluate_rag.py
│
├── tests/
│   ├── test_document_parser.py
│   ├── test_document_parser_pdf.py
│   ├── test_rag_evaluation.py
│   └── test_retrieval_threshold.py
│
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
API

The application exposes a REST API through FastAPI.

Authentication
Register
POST /auth/register

Creates a new user account.

Login
POST /auth/login

Authenticates a user and returns a JWT access token.

Documents
Create Document
POST /documents/

Creates a document from JSON input.

List Documents
GET /documents/

Returns documents belonging to the authenticated user.

Get Document
GET /documents/{document_id}

Returns a specific document belonging to the authenticated user.

Upload Document
POST /documents/upload

Uploads and processes a TXT or PDF document.

The upload pipeline automatically:

Validates the file type
Reads the file
Extracts the text
Creates the document
Splits the document into chunks
Generates embeddings
Stores the chunks and embeddings
Associates the document with the authenticated user
AI
Generate AI Response
POST /ai/generate

Sends a prompt directly to the local language model.

Ask Knowledge Base
POST /ai/ask

Uses the complete RAG pipeline:

Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Relevant Chunks
   ↓
Context
   ↓
Qwen3
   ↓
Answer
Database Architecture

KnowledgeHub AI uses PostgreSQL as its primary database.

The current database contains the main entities:

users
documents
document_chunks

Relationships:

User
 │
 └───< Documents
           │
           └───< Document Chunks

Each document belongs to a user.

Each document can contain multiple chunks.

Each chunk can contain a vector embedding.

Database Migrations

Database schema changes are managed using Alembic.

Migration commands:

alembic upgrade head

Check the current migration:

alembic current

Check for schema differences:

alembic check

Create a migration:

alembic revision --autogenerate -m "description"
Running the Project Locally
1. Clone the Repository
git clone https://github.com/Amer-Omar-Bamazrou/knowledgehub-ai.git
cd knowledgehub-ai
2. Create a Virtual Environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1
3. Install Dependencies
pip install -r requirements.txt
4. Start PostgreSQL

The project includes Docker configuration for PostgreSQL.

docker compose up -d

Check the running containers:

docker ps
5. Run Database Migrations
alembic upgrade head
6. Start Ollama

Make sure Ollama is installed and running.

The project currently expects:

qwen3:4b

and:

nomic-embed-text

Pull the models if necessary:

ollama pull qwen3:4b
ollama pull nomic-embed-text
7. Start FastAPI
uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000
API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

Swagger can be used to test:

Authentication
Document creation
Document uploads
AI generation
RAG queries
Testing

The project uses pytest.

Run the complete test suite:

pytest

The current test suite covers areas including:

TXT document parsing
PDF document parsing
Retrieval relevance
RAG evaluation
Unknown-question handling

Example:

6 passed
RAG Evaluation

KnowledgeHub AI includes an evaluation script for testing the RAG pipeline.

Run:

python -m scripts.evaluate_rag

The evaluation tests questions against the knowledge base and checks whether the retrieval system behaves as expected.

Example evaluation:

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

The evaluation is intended to provide a repeatable way of checking RAG behaviour as the system evolves.

Example RAG Workflow

Suppose a user uploads a document containing:

FastAPI is a Python web framework used to build modern APIs.
PostgreSQL is a relational database used to store application data.
SQLAlchemy is a Python ORM used to interact with relational databases.

The document is processed into chunks and embedded.

The user can then ask:

What framework is used to build the API?

KnowledgeHub AI performs semantic retrieval and passes the relevant document context to Qwen3.

The resulting answer can be:

FastAPI

The important part is that the answer is generated using information retrieved from the user's knowledge base rather than relying solely on the model's general knowledge.

Security

The project currently includes several security-related mechanisms:

Password hashing with Argon2
JWT-based authentication
OAuth2 password authentication
Protected API routes
User-specific document ownership
User-level retrieval isolation
Relevance filtering before RAG generation

Sensitive configuration is stored through environment variables rather than being hard-coded into application logic.

Current Development Status

KnowledgeHub AI has progressed through the core backend and RAG implementation stages.

Backend Foundation
 FastAPI application
 Application structure
 Configuration management
 REST API
Database
 PostgreSQL
 SQLAlchemy
 Alembic
 Database migrations
 pgvector
 Document chunks
 Vector embeddings
Authentication
 User registration
 Password hashing
 JWT authentication
 OAuth2 login
 Protected routes
 User document ownership
 User isolation
Document Intelligence
 TXT ingestion
 PDF ingestion
 PDF text extraction
 Document chunking
 Embedding generation
 Vector storage
RAG
 Question embeddings
 Semantic retrieval
 Cosine similarity
 Relevance threshold
 Context construction
 LLM generation
 Knowledge-base question answering
 RAG evaluation
Testing
 Unit tests
 PDF parser tests
 Retrieval tests
 RAG evaluation
 Unknown-question testing
Roadmap

The project will continue toward a more production-oriented Generative AI architecture.

Phase 1 — Backend Foundation
 FastAPI
 Python
 REST API
 Project architecture
Phase 2 — Database
 PostgreSQL
 SQLAlchemy
 Alembic
 pgvector
Phase 3 — Authentication
 User registration
 JWT authentication
 Password hashing
 Protected endpoints
 User isolation
Phase 4 — Document Processing
 TXT ingestion
 PDF ingestion
 Text extraction
 Chunking
Phase 5 — Semantic Search
 Embeddings
 Vector storage
 Similarity search
 Relevance threshold
Phase 6 — RAG
 Retrieval pipeline
 Context construction
 LLM generation
 Knowledge-base Q&A
 RAG evaluation
Phase 7 — Production Hardening
 Improved API error handling
 Structured logging
 Better configuration management
 Rate limiting
 Improved document validation
 More comprehensive integration tests
 CI/CD
 Production deployment
Phase 8 — Advanced RAG
 Improved chunking strategies
 Metadata filtering
 Hybrid search
 Reranking
 Improved source citations
 RAG evaluation datasets
 Retrieval metrics
Phase 9 — AI Agents
 LangGraph
 Tool calling
 Agent workflows
 Guardrails
 Agent evaluation
 Multi-step reasoning workflows
Engineering Goals

KnowledgeHub AI is being developed with several engineering goals in mind:

Backend Engineering

Build a strong foundation in:

API design
Database architecture
Authentication
ORM usage
Migrations
Testing
Docker
Production deployment
Generative AI Engineering

Develop practical experience with:

LLM integration
Local inference
Embeddings
Vector databases
Semantic search
RAG
Evaluation
AI application architecture
Agent workflows
Production Engineering

The long-term goal is to move the project beyond a simple AI prototype toward a maintainable production-oriented system.

Project Philosophy

KnowledgeHub AI follows a practical engineering approach:

Learn
  ↓
Build
  ↓
Test
  ↓
Evaluate
  ↓
Improve
  ↓
Deploy

The focus is on understanding how the individual components work together rather than simply integrating AI APIs into an application.

Author

Amer Omar Bamazrou

Software Engineering Graduate
First Class Honours — De Montfort University

GitHub:

https://github.com/Amer-Omar-Bamazrou

Project:

https://github.com/Amer-Omar-Bamazrou/knowledgehub-ai
```
