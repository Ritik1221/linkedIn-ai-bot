# LinkedIn AI Agent

An AI-powered job search assistant that helps you find, track, and apply for jobs on LinkedIn.

## Project Structure

The project consists of two main components:

- `linkedin-agent-frontend`: Next.js frontend application
- `linkedin-agent-backend`: FastAPI backend application

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- LinkedIn Developer Account (for OAuth)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-agent.git
   cd linkedin-agent
   ```

2. Copy the example environment file and update it with your values:
   ```bash
   cp .env.example .env
   ```

3. Set up LinkedIn OAuth:
   - Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
   - Create a new application
   - Add OAuth 2.0 redirect URLs:
     - `http://localhost:3000/api/auth/callback/linkedin` (development)
     - Your production URL (when deploying)
   - Copy the Client ID and Client Secret to your `.env` file

4. Start the development environment:
   ```bash
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL database
   - Redis cache
   - Backend API (FastAPI)
   - Celery worker
   - Flower (Celery monitoring)
   - Frontend (Next.js)

5. Access the applications:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Flower Dashboard: http://localhost:5555

## Development

### Frontend Development

The frontend is built with:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- NextAuth.js for authentication
- Axios for API communication

To run the frontend locally:
```bash
cd linkedin-agent-frontend
npm install
npm run dev
```

### Backend Development

The backend is built with:
- FastAPI
- PostgreSQL
- Redis
- Celery
- SQLAlchemy

To run the backend locally:
```bash
cd linkedin-agent-backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Environment Variables

### Required Variables

Frontend:
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXTAUTH_URL`: Frontend URL
- `NEXTAUTH_SECRET`: Random string for session encryption
- `LINKEDIN_CLIENT_ID`: LinkedIn OAuth Client ID
- `LINKEDIN_CLIENT_SECRET`: LinkedIn OAuth Client Secret

Backend:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `LINKEDIN_CLIENT_ID`: LinkedIn OAuth Client ID
- `LINKEDIN_CLIENT_SECRET`: LinkedIn OAuth Client Secret

## Docker Development

The development environment uses Docker Compose with the following features:
- Hot reloading for both frontend and backend
- Volume mounting for local development
- Health checks for all services
- Automatic dependency installation
- Development-specific configurations

### Useful Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up -d --build

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Testing

```bash
# Frontend tests
cd linkedin-agent-frontend
npm test

# Backend tests
cd linkedin-agent-backend
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 