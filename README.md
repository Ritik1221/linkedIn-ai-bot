# LinkedIn AI Agent

An AI-powered platform for enhancing LinkedIn job search, profile optimization, and networking.

## Overview

LinkedIn AI Agent is a comprehensive platform that leverages artificial intelligence to help users optimize their LinkedIn profiles, find relevant job opportunities, automate job applications, and enhance networking. The platform consists of a FastAPI backend and a Next.js frontend.

## Components

### Backend

The backend provides a RESTful API for managing user data, LinkedIn integration, and AI-powered features. It's built with FastAPI, PostgreSQL, SQLAlchemy, and Celery.

Key features:
- User authentication with JWT and LinkedIn OAuth
- LinkedIn profile synchronization and analysis
- Job search and matching algorithms
- Application tracking and automation
- AI-powered content generation (cover letters, messages)
- Background task processing with Celery

[View Backend Documentation](linkedin-agent-backend/README.md)

### Frontend

The frontend provides an intuitive user interface for interacting with the LinkedIn AI Agent platform. It's built with Next.js, TypeScript, Redux, and Tailwind CSS.

Key features:
- Responsive, modern UI with dark/light mode
- Secure authentication with NextAuth.js
- Interactive job search and filtering
- Application tracking dashboard
- Profile optimization suggestions
- Networking management

[View Frontend Documentation](linkedin-agent-frontend/README.md)

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Next.js        │     │  FastAPI        │     │  Celery         │
│  Frontend       │────▶│  Backend        │────▶│  Workers        │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                        │
                               ▼                        ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │                 │     │                 │
                        │  PostgreSQL     │     │  Redis          │
                        │  Database       │     │  Cache/Queue    │
                        │                 │     │                 │
                        └─────────────────┘     └─────────────────┘
                               │                        │
                               └────────────┬───────────┘
                                            ▼
                                   ┌─────────────────┐
                                   │                 │
                                   │  AI Services    │
                                   │  (LLM, Vector DB)│
                                   │                 │
                                   └─────────────────┘
```

## Getting Started

### Prerequisites

- Docker and Docker Compose (for containerized setup)
- Python 3.11+ (for backend development)
- Node.js 18+ (for frontend development)
- PostgreSQL
- Redis

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-agent.git
   cd linkedin-agent
   ```

2. Create environment files:
   ```bash
   cp linkedin-agent-backend/.env.example linkedin-agent-backend/.env
   cp linkedin-agent-frontend/.env.example linkedin-agent-frontend/.env
   ```

3. Update the environment files with your configuration.

4. Start the services:
   ```bash
   docker-compose up -d
   ```

5. Run backend migrations:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

6. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/v1
   - API Documentation: http://localhost:8000/api/v1/docs

### Local Development

For detailed instructions on setting up local development environments, see:
- [Backend Setup](linkedin-agent-backend/README.md#setup)
- [Frontend Setup](linkedin-agent-frontend/README.md#setup)

## Features

- **Profile Optimization**: AI-powered analysis and suggestions for LinkedIn profiles
- **Job Matching**: Intelligent job recommendations based on skills and experience
- **Application Automation**: Streamlined job application process with AI-generated content
- **Networking Enhancement**: Smart connection suggestions and message templates
- **Analytics Dashboard**: Track job search progress and application success rates

## License

[MIT License](LICENSE) 