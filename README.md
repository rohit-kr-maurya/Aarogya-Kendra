# Aarogya Kendra - Clinical AI Backend Engine

A robust, enterprise-grade clinical management and AI-assisted acupressure diagnostic backend built with FastAPI, PostgreSQL (Supabase), and Google Gemini AI.

## Architecture Highlights
- **FastAPI Core**: Asynchronous RESTful API endpoints for patient records and visit history.
- **Relational Persistence**: SQLAlchemy ORM integrated with hosted PostgreSQL on Supabase (Session Pooler).
- **Dual-Tier Resilient AI Failover**: Primary diagnosis routed via Gemini 3.1 Flash Lite, automatically falling back to Flash-Lite under latency/rate-limit pressures.
- **Data Integrity**: Strict runtime input/output validation powered by Pydantic v2 schemas.

## Tech Stack
- **Language**: Python 3.14
- **Framework**: FastAPI / Uvicorn
- **ORM & DB**: SQLAlchemy, Psycopg 3, Supabase PostgreSQL
- **AI Integration**: Google GenAI SDK (Gemini Models)
