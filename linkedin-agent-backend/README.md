# LinkedIn AI Agent Backend

An AI-powered backend service for enhancing LinkedIn job search, profile optimization, and networking.

## Overview

The LinkedIn AI Agent backend provides a comprehensive API for managing LinkedIn profiles, job searches, applications, and networking. It leverages AI to analyze profiles, match jobs, and generate personalized content for job applications.

## Features

- **User Authentication**: Secure login with email/password and LinkedIn OAuth
- **Profile Management**: Store and analyze LinkedIn profiles
- **Job Search**: Find and track relevant job opportunities
- **Application Tracking**: Manage job applications and track their status
- **AI-Powered Assistance**: 
  - Profile analysis and optimization suggestions
  - Job matching based on skills and experience
  - Automated cover letter generation
  - Resume tailoring for specific job applications
- **Networking**: Manage connections and messages

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens, OAuth2
- **Task Queue**: Celery with Redis
- **AI/ML**: LangChain, OpenAI, Anthropic
- **Vector Database**: Pinecone
- **Testing**: Pytest
- **Containerization**: Docker
- **Migration**: Alembic

## Project Structure

```
linkedin-agent-backend/
├── migrations/           # Database migrations
├── src/
│   ├── app/              # Main application
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── db/           # Database configuration
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # Application entry point
│   └── worker/           # Celery worker
│       ├── tasks/        # Background tasks
│       └── main.py       # Worker entry point
├── tests/                # Test suite
├── .env                  # Environment variables
├── .env.example          # Example environment variables
├── alembic.ini           # Alembic configuration
├── Dockerfile.dev        # Development Dockerfile
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-agent.git
   cd linkedin-agent/linkedin-agent-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and fill in your configuration.

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the API server:
   ```bash
   uvicorn src.app.main:app --reload
   ```

7. Start the Celery worker:
   ```bash
   celery -A src.worker.main worker --loglevel=info
   ```

### Docker Development

1. Build and start the containers:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. Run migrations:
   ```bash
   docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
   ```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Testing

Run the test suite:

```bash
pytest
```

## License

[MIT License](LICENSE) 