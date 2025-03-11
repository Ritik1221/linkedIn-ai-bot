# LinkedIn AI Agent Backend

A high-performance, secure API backend for the LinkedIn AI Agent platform.

## Overview

The LinkedIn AI Agent backend provides the API and services for managing LinkedIn profiles, job searches, applications, and networking. It integrates with the LinkedIn API and uses AI technologies to provide personalized insights and recommendations.

## Features

- **User Authentication**: Secure authentication with JWT and LinkedIn OAuth
- **Profile Management**: LinkedIn profile synchronization and storage
- **Job Search**: Advanced job search and recommendation algorithms
- **Application Tracking**: Comprehensive application management
- **AI-Powered Features**:
  - Profile optimization suggestions
  - Job matching algorithm
  - Cover letter generation
  - Resume tailoring
- **Performance Optimization**:
  - Redis caching for API responses
  - GZip compression middleware
  - Request timing monitoring
  - Database query optimization
  - Connection pooling
- **Security Enhancements**:
  - Rate limiting for API endpoints
  - CORS protection
  - Input validation with Pydantic
  - Secure headers middleware

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL, SQLAlchemy ORM
- **Caching**: Redis
- **Task Queue**: Celery
- **Authentication**: JWT, OAuth2
- **AI Models**: OpenAI GPT-4
- **Testing**: Pytest
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker

## Project Structure

```
linkedin-agent-backend/
├── app/
│   ├── api/             # API endpoints
│   │   ├── v1/          # API version 1
│   ├── core/            # Core configurations
│   │   ├── config.py    # Environment variables
│   │   ├── security.py  # Authentication utilities
│   │   └── middleware/  # Custom middleware components
│   ├── db/              # Database models and session
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic services
│   ├── tasks/           # Background tasks
│   ├── utils/           # Utility functions
│   └── main.py          # Application entry point
├── alembic/             # Database migrations
├── tests/               # Test suite
├── docker/              # Docker configurations
├── .env                 # Environment variables
├── .env.example         # Example environment variables
├── Dockerfile           # Main Dockerfile
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
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

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and configure your environment variables.

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

### Docker Development

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Performance Considerations

The backend is optimized for performance through several strategies:

- **Database Optimization**: Efficient queries, proper indexing, and connection pooling
- **Caching**: Redis caching for frequent API requests and session data
- **Compression**: GZip compression to reduce response payload size
- **Monitoring**: Request timing middleware to track and analyze performance bottlenecks

## Security Features

Security is a priority with several implemented features:

- **Rate Limiting**: Protection against abuse and DoS attacks
- **Input Validation**: Strict schema validation with Pydantic
- **Authentication**: Secure JWT implementation with refresh tokens
- **CORS**: Configured Cross-Origin Resource Sharing
- **Secure Headers**: Protection against common web vulnerabilities

## Testing

Run the test suite:

```bash
pytest
```

## API Documentation

The API is documented using Swagger/OpenAPI. When the server is running, you can access:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## License

[MIT License](LICENSE) 