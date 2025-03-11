"""
Base module for database models.
Import all models here for Alembic to detect them.
"""

from src.app.db.session import Base

# Import all models here for Alembic
from src.app.models.user import User
from src.app.models.profile import Profile, Experience, Education, Certification
from src.app.models.job import Job, SavedJob, JobMatch
from src.app.models.application import Application, ApplicationStatusUpdate, Resume, CoverLetter
# from src.app.models.job import Job
# from src.app.models.application import Application 