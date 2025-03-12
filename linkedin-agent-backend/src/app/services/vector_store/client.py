"""
Vector store client for the LinkedIn AI Agent.
This module provides functions for semantic search and vector-based job matching.
"""

import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np

from sqlalchemy.orm import Session

from src.app.db.session import SessionLocal
from src.app.models.profile import Profile
from src.app.models.job import Job
from src.app.core.config import settings

# Import embedding models - we'll support multiple providers
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import sentence_transformers
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

logger = logging.getLogger(__name__)


class VectorStoreService:
    """Vector store service for semantic search and job matching."""

    def __init__(self, db: Session = None):
        """
        Initialize the vector store service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.embedding_model = settings.EMBEDDING_MODEL
        self.embedding_provider = settings.EMBEDDING_PROVIDER.lower()
        self.vector_store_provider = settings.VECTOR_STORE_PROVIDER.lower()
        self.vector_dimension = settings.VECTOR_DIMENSION
        
        # Initialize embedding model
        if self.embedding_provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI package not installed. Install with 'pip install openai'.")
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.embedding_provider == "sentence_transformers":
            if not SENTENCE_TRANSFORMERS_AVAILABLE:
                raise ImportError("Sentence Transformers package not installed. Install with 'pip install sentence-transformers'.")
            self.embedding_model = sentence_transformers.SentenceTransformer(self.embedding_model)
        else:
            raise ValueError(f"Unsupported embedding provider: {self.embedding_provider}")
        
        # Initialize vector store
        if self.vector_store_provider == "pinecone":
            if not PINECONE_AVAILABLE:
                raise ImportError("Pinecone package not installed. Install with 'pip install pinecone-client'.")
            pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT)
            
            # Check if index exists, if not create it
            if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                pinecone.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=self.vector_dimension,
                    metric="cosine"
                )
            
            self.index = pinecone.Index(settings.PINECONE_INDEX_NAME)
        elif self.vector_store_provider == "in_memory":
            # Simple in-memory vector store for development
            self.vectors = {}
            self.metadata = {}
        else:
            raise ValueError(f"Unsupported vector store provider: {self.vector_store_provider}")

    def get_embedding(self, text: str) -> List[float]:
        """
        Get embeddings for text using the configured provider.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if self.embedding_provider == "openai":
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        elif self.embedding_provider == "sentence_transformers":
            return self.embedding_model.encode(text).tolist()
        else:
            raise ValueError(f"Unsupported embedding provider: {self.embedding_provider}")

    def index_job(self, job: Job) -> bool:
        """
        Index a job in the vector store.
        
        Args:
            job: Job to index
            
        Returns:
            True if indexing was successful
        """
        try:
            # Create job text representation
            job_text = f"""
            Title: {job.title}
            Company: {job.company}
            Location: {job.location}
            Description: {job.description}
            """
            
            # Get embedding
            embedding = self.get_embedding(job_text)
            
            # Store in vector database
            job_id = str(job.id)
            metadata = {
                "id": job_id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "type": "job"
            }
            
            if self.vector_store_provider == "pinecone":
                self.index.upsert(
                    vectors=[(job_id, embedding, metadata)],
                    namespace="jobs"
                )
            elif self.vector_store_provider == "in_memory":
                self.vectors[job_id] = embedding
                self.metadata[job_id] = metadata
            
            return True
        except Exception as e:
            logger.error(f"Error indexing job: {str(e)}")
            return False

    def index_profile(self, profile: Profile) -> bool:
        """
        Index a profile in the vector store.
        
        Args:
            profile: Profile to index
            
        Returns:
            True if indexing was successful
        """
        try:
            # Create profile text representation
            skills_text = ", ".join([skill.name for skill in profile.skills]) if hasattr(profile, "skills") and profile.skills else ""
            experiences_text = ""
            
            if hasattr(profile, "experiences") and profile.experiences:
                for exp in profile.experiences:
                    experiences_text += f"{exp.title} at {exp.company}, {exp.description}\n"
            
            profile_text = f"""
            Name: {profile.full_name}
            Headline: {profile.headline}
            Summary: {profile.summary}
            Skills: {skills_text}
            Experience: {experiences_text}
            """
            
            # Get embedding
            embedding = self.get_embedding(profile_text)
            
            # Store in vector database
            profile_id = str(profile.id)
            metadata = {
                "id": profile_id,
                "name": profile.full_name,
                "headline": profile.headline,
                "type": "profile"
            }
            
            if self.vector_store_provider == "pinecone":
                self.index.upsert(
                    vectors=[(profile_id, embedding, metadata)],
                    namespace="profiles"
                )
            elif self.vector_store_provider == "in_memory":
                self.vectors[profile_id] = embedding
                self.metadata[profile_id] = metadata
            
            return True
        except Exception as e:
            logger.error(f"Error indexing profile: {str(e)}")
            return False

    def find_similar_jobs(
        self, 
        profile_id: str, 
        limit: int = 10, 
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Find jobs similar to a profile.
        
        Args:
            profile_id: Profile ID to match against
            limit: Maximum number of results
            min_score: Minimum similarity score (0-1)
            
        Returns:
            List of similar jobs with scores
        """
        try:
            # Get profile
            profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
            if not profile:
                return []
            
            # Create profile text representation
            skills_text = ", ".join([skill.name for skill in profile.skills]) if hasattr(profile, "skills") and profile.skills else ""
            experiences_text = ""
            
            if hasattr(profile, "experiences") and profile.experiences:
                for exp in profile.experiences:
                    experiences_text += f"{exp.title} at {exp.company}, {exp.description}\n"
            
            profile_text = f"""
            Name: {profile.full_name}
            Headline: {profile.headline}
            Summary: {profile.summary}
            Skills: {skills_text}
            Experience: {experiences_text}
            """
            
            # Get embedding
            query_embedding = self.get_embedding(profile_text)
            
            # Query vector database
            if self.vector_store_provider == "pinecone":
                results = self.index.query(
                    vector=query_embedding,
                    top_k=limit,
                    namespace="jobs",
                    include_metadata=True
                )
                
                # Process results
                matches = []
                for match in results["matches"]:
                    if match["score"] >= min_score:
                        job_id = match["id"]
                        job = self.db.query(Job).filter(Job.id == job_id).first()
                        if job:
                            matches.append({
                                "id": job.id,
                                "title": job.title,
                                "company": job.company,
                                "location": job.location,
                                "score": match["score"]
                            })
                
                return matches
            elif self.vector_store_provider == "in_memory":
                # Simple cosine similarity implementation
                results = []
                for job_id, job_vector in self.vectors.items():
                    metadata = self.metadata.get(job_id)
                    if metadata and metadata.get("type") == "job":
                        # Calculate cosine similarity
                        similarity = self._cosine_similarity(query_embedding, job_vector)
                        if similarity >= min_score:
                            job = self.db.query(Job).filter(Job.id == job_id).first()
                            if job:
                                results.append({
                                    "id": job.id,
                                    "title": job.title,
                                    "company": job.company,
                                    "location": job.location,
                                    "score": similarity
                                })
                
                # Sort by score descending and limit
                results.sort(key=lambda x: x["score"], reverse=True)
                return results[:limit]
            
            return []
        except Exception as e:
            logger.error(f"Error finding similar jobs: {str(e)}")
            return []

    def search_jobs(
        self, 
        query: str, 
        limit: int = 10, 
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for jobs using semantic search.
        
        Args:
            query: Search query
            limit: Maximum number of results
            min_score: Minimum similarity score (0-1)
            
        Returns:
            List of job matches with scores
        """
        try:
            # Get embedding for query
            query_embedding = self.get_embedding(query)
            
            # Query vector database
            if self.vector_store_provider == "pinecone":
                results = self.index.query(
                    vector=query_embedding,
                    top_k=limit,
                    namespace="jobs",
                    include_metadata=True
                )
                
                # Process results
                matches = []
                for match in results["matches"]:
                    if match["score"] >= min_score:
                        job_id = match["id"]
                        job = self.db.query(Job).filter(Job.id == job_id).first()
                        if job:
                            matches.append({
                                "id": job.id,
                                "title": job.title,
                                "company": job.company,
                                "location": job.location,
                                "score": match["score"]
                            })
                
                return matches
            elif self.vector_store_provider == "in_memory":
                # Simple cosine similarity implementation
                results = []
                for job_id, job_vector in self.vectors.items():
                    metadata = self.metadata.get(job_id)
                    if metadata and metadata.get("type") == "job":
                        # Calculate cosine similarity
                        similarity = self._cosine_similarity(query_embedding, job_vector)
                        if similarity >= min_score:
                            job = self.db.query(Job).filter(Job.id == job_id).first()
                            if job:
                                results.append({
                                    "id": job.id,
                                    "title": job.title,
                                    "company": job.company,
                                    "location": job.location,
                                    "score": similarity
                                })
                
                # Sort by score descending and limit
                results.sort(key=lambda x: x["score"], reverse=True)
                return results[:limit]
            
            return []
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
            return []

    def find_similar_profiles(
        self, 
        job_id: str, 
        limit: int = 10, 
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Find profiles similar to a job.
        
        Args:
            job_id: Job ID to match against
            limit: Maximum number of results
            min_score: Minimum similarity score (0-1)
            
        Returns:
            List of similar profiles with scores
        """
        try:
            # Get job
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return []
            
            # Create job text representation
            job_text = f"""
            Title: {job.title}
            Company: {job.company}
            Location: {job.location}
            Description: {job.description}
            """
            
            # Get embedding
            query_embedding = self.get_embedding(job_text)
            
            # Query vector database
            if self.vector_store_provider == "pinecone":
                results = self.index.query(
                    vector=query_embedding,
                    top_k=limit,
                    namespace="profiles",
                    include_metadata=True
                )
                
                # Process results
                matches = []
                for match in results["matches"]:
                    if match["score"] >= min_score:
                        profile_id = match["id"]
                        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
                        if profile:
                            matches.append({
                                "id": profile.id,
                                "name": profile.full_name,
                                "headline": profile.headline,
                                "user_id": profile.user_id,
                                "score": match["score"]
                            })
                
                return matches
            elif self.vector_store_provider == "in_memory":
                # Simple cosine similarity implementation
                results = []
                for profile_id, profile_vector in self.vectors.items():
                    metadata = self.metadata.get(profile_id)
                    if metadata and metadata.get("type") == "profile":
                        # Calculate cosine similarity
                        similarity = self._cosine_similarity(query_embedding, profile_vector)
                        if similarity >= min_score:
                            profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
                            if profile:
                                results.append({
                                    "id": profile.id,
                                    "name": profile.full_name,
                                    "headline": profile.headline,
                                    "user_id": profile.user_id,
                                    "score": similarity
                                })
                
                # Sort by score descending and limit
                results.sort(key=lambda x: x["score"], reverse=True)
                return results[:limit]
            
            return []
        except Exception as e:
            logger.error(f"Error finding similar profiles: {str(e)}")
            return []

    def hybrid_search_jobs(
        self,
        query: str,
        keywords: List[str] = None,
        location: str = None,
        limit: int = 10,
        semantic_weight: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword search.
        
        Args:
            query: Search query
            keywords: List of keywords to filter by
            location: Location to filter by
            limit: Maximum number of results
            semantic_weight: Weight for semantic search (0-1)
            
        Returns:
            List of job matches with scores
        """
        try:
            # Get semantic search results
            semantic_results = self.search_jobs(query, limit=limit * 2)
            
            # Filter by location if provided
            if location:
                semantic_results = [
                    result for result in semantic_results
                    if location.lower() in result.get("location", "").lower()
                ]
            
            # Filter by keywords if provided
            if keywords and len(keywords) > 0:
                filtered_results = []
                for result in semantic_results:
                    job = self.db.query(Job).filter(Job.id == result["id"]).first()
                    if job:
                        # Check if any keyword is in title or description
                        job_text = f"{job.title} {job.description}".lower()
                        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in job_text)
                        if keyword_matches > 0:
                            # Adjust score based on keyword matches
                            keyword_score = keyword_matches / len(keywords)
                            combined_score = (semantic_weight * result["score"]) + ((1 - semantic_weight) * keyword_score)
                            result["score"] = combined_score
                            filtered_results.append(result)
                
                semantic_results = filtered_results
            
            # Sort by score descending and limit
            semantic_results.sort(key=lambda x: x["score"], reverse=True)
            return semantic_results[:limit]
        except Exception as e:
            logger.error(f"Error performing hybrid search: {str(e)}")
            return []

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity (0-1)
        """
        # Convert to numpy arrays
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        
        return dot_product / (norm_vec1 * norm_vec2)
    
    def reindex_all_jobs(self) -> Tuple[int, int]:
        """
        Reindex all jobs in the database.
        
        Returns:
            Tuple of (success_count, total_count)
        """
        try:
            # Get all jobs
            jobs = self.db.query(Job).all()
            
            total_count = len(jobs)
            success_count = 0
            
            for job in jobs:
                if self.index_job(job):
                    success_count += 1
            
            return (success_count, total_count)
        except Exception as e:
            logger.error(f"Error reindexing jobs: {str(e)}")
            return (0, 0)
    
    def reindex_all_profiles(self) -> Tuple[int, int]:
        """
        Reindex all profiles in the database.
        
        Returns:
            Tuple of (success_count, total_count)
        """
        try:
            # Get all profiles
            profiles = self.db.query(Profile).all()
            
            total_count = len(profiles)
            success_count = 0
            
            for profile in profiles:
                if self.index_profile(profile):
                    success_count += 1
            
            return (success_count, total_count)
        except Exception as e:
            logger.error(f"Error reindexing profiles: {str(e)}")
            return (0, 0)


def get_vector_store_service(db: Session = None) -> VectorStoreService:
    """
    Get a vector store service instance.
    
    Args:
        db: Database session
        
    Returns:
        Vector store service instance
    """
    if db is None:
        db = SessionLocal()
    return VectorStoreService(db=db) 