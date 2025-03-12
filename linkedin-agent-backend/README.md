# LinkedIn AI Agent Backend

An intelligent agent for automating LinkedIn job search, application processes, and professional networking. This agent uses AI to customize resumes, generate cover letters, and match job opportunities to your skills and experiences.

## Features

- **Automated LinkedIn Profile Synchronization**: Keep your system profile updated with your latest LinkedIn information
- **Intelligent Job Matching**: Find the most suitable jobs based on your skills, experience, and preferences
- **Resume Customization**: Automatically generate tailored resumes for specific job postings
- **Cover Letter Generation**: Create personalized cover letters highlighting your relevant experience
- **Application Tracking**: Monitor the status of your job applications
- **Scheduled Operations**: Regular background tasks handle profile syncing, job searching, and more

## System Architecture

The backend system consists of the following components:

1. **API Service**: RESTful API for client applications
2. **Worker Service**: Background task processing with Celery
3. **Scheduler**: Periodic task scheduling with Celery Beat
4. **Monitoring API**: Health checks and metrics for system monitoring

### Core Services

- **LinkedIn Service**: Integration with LinkedIn API for profile and job data
- **LLM Service**: Integration with language models for content generation and analysis
- **Vector Store Service**: Fast semantic search for job matching
- **Automation Service**: Application and resume generation workflows

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Celery 5+

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/linkedin-agent-backend.git
cd linkedin-agent-backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
# Copy the sample environment file
cp scripts/celery.env.sample /etc/linkedin-agent/celery.env
# Edit the environment file with your configuration
nano /etc/linkedin-agent/celery.env
```

5. Create the database:

```bash
# Using psql
psql -U postgres
CREATE DATABASE linkedin_agent;
```

6. Run migrations:

```bash
# Using alembic
alembic upgrade head
```

### Running the Services

#### Development Environment

1. Start the API server:

```bash
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the Celery worker:

```bash
celery -A src.worker.main worker --loglevel=INFO
```

3. Start the Celery beat scheduler:

```bash
celery -A src.worker.main beat --loglevel=INFO
```

4. Start the monitoring API:

```bash
gunicorn src.worker.api:app --bind 0.0.0.0:8001 --workers 2
```

#### Production Environment

Use the provided systemd service files:

1. Copy the service files:

```bash
sudo cp scripts/celery-worker.service /etc/systemd/system/
sudo cp scripts/celery-beat.service /etc/systemd/system/
sudo cp scripts/celery-api.service /etc/systemd/system/
```

2. Create a celery user and group:

```bash
sudo useradd -r -s /bin/false celery
sudo mkdir -p /etc/linkedin-agent
sudo chown celery:celery /etc/linkedin-agent
```

3. Copy and edit the environment file:

```bash
sudo cp scripts/celery.env.sample /etc/linkedin-agent/celery.env
sudo chown celery:celery /etc/linkedin-agent/celery.env
sudo chmod 600 /etc/linkedin-agent/celery.env
sudo nano /etc/linkedin-agent/celery.env
```

4. Start and enable the services:

```bash
sudo systemctl daemon-reload
sudo systemctl start celery-worker.service
sudo systemctl start celery-beat.service
sudo systemctl start celery-api.service
sudo systemctl enable celery-worker.service
sudo systemctl enable celery-beat.service
sudo systemctl enable celery-api.service
```

5. Check the status:

```bash
sudo systemctl status celery-worker.service
sudo systemctl status celery-beat.service
sudo systemctl status celery-api.service
```

## Monitoring

The system includes a monitoring API that provides health checks and metrics.

- Health check endpoint: `http://localhost:8001/health`
- Metrics endpoint: `http://localhost:8001/metrics`
- Task status endpoint: `http://localhost:8001/task/<task_id>`
- Task report endpoint: `http://localhost:8001/report`
- Custom metrics endpoint: `http://localhost:8001/custom-metrics`

## Configuration

The system can be configured using environment variables. See `scripts/celery.env.sample` for a list of available configuration options.

## Development

### Project Structure

```
linkedin-agent-backend/
├── src/
│   ├── app/              # FastAPI application
│   │   ├── api/          # API endpoints
│   │   ├── db/           # Database models and session
│   │   ├── models/       # Pydantic models
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app entry point
│   ├── worker/           # Celery worker
│   │   ├── tasks/        # Celery tasks
│   │   ├── api.py        # Worker API
│   │   ├── main.py       # Celery app entry point
│   │   └── monitoring.py # Monitoring utilities
│   └── utils/            # Utility functions
├── scripts/              # Scripts for deployment
├── alembic/              # Database migrations
├── tests/                # Unit and integration tests
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

### Testing

Run the tests with pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for GPT models
- FastAPI for the web framework
- Celery for task processing
- LinkedIn for the API 