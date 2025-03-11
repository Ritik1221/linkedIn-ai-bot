"""
LinkedIn API client for the LinkedIn AI Agent.
This module provides functions for interacting with the LinkedIn API.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import requests
from fastapi import HTTPException, status

from src.app.core.config import settings

logger = logging.getLogger(__name__)

# LinkedIn API endpoints
LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_PROFILE_URL = "https://api.linkedin.com/v2/me"
LINKEDIN_EMAIL_URL = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
LINKEDIN_PROFILE_PICTURE_URL = "https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~:playableStreams))"
LINKEDIN_JOBS_URL = "https://api.linkedin.com/v2/jobSearch"


class LinkedInClient:
    """LinkedIn API client."""

    def __init__(
        self,
        client_id: str = settings.LINKEDIN_CLIENT_ID,
        client_secret: str = settings.LINKEDIN_CLIENT_SECRET,
        redirect_uri: str = settings.LINKEDIN_REDIRECT_URI,
    ):
        """
        Initialize the LinkedIn client.
        
        Args:
            client_id: LinkedIn client ID
            client_secret: LinkedIn client secret
            redirect_uri: LinkedIn redirect URI
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, state: str = None) -> str:
        """
        Get the LinkedIn authorization URL.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            LinkedIn authorization URL
        """
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "r_liteprofile r_emailaddress w_member_social",
        }
        
        if state:
            params["state"] = state
            
        return f"{LINKEDIN_AUTH_URL}?{urlencode(params)}"

    def get_access_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from LinkedIn
            
        Returns:
            Dict containing access token and related information
            
        Raises:
            HTTPException: If token exchange fails
        """
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        
        try:
            response = requests.post(LINKEDIN_TOKEN_URL, data=payload)
            response.raise_for_status()
            token_data = response.json()
            
            # Add expiration timestamp
            token_data["expires_at"] = int(time.time()) + token_data.get("expires_in", 0)
            
            return token_data
        except requests.RequestException as e:
            logger.error(f"LinkedIn token exchange failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"LinkedIn token exchange failed: {str(e)}",
            )

    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an expired access token.
        
        Args:
            refresh_token: Refresh token from previous authentication
            
        Returns:
            Dict containing new access token and related information
            
        Raises:
            HTTPException: If token refresh fails
        """
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        
        try:
            response = requests.post(LINKEDIN_TOKEN_URL, data=payload)
            response.raise_for_status()
            token_data = response.json()
            
            # Add expiration timestamp
            token_data["expires_at"] = int(time.time()) + token_data.get("expires_in", 0)
            
            return token_data
        except requests.RequestException as e:
            logger.error(f"LinkedIn token refresh failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"LinkedIn token refresh failed: {str(e)}",
            )

    def get_profile(self, access_token: str) -> Dict[str, Any]:
        """
        Get user's LinkedIn profile.
        
        Args:
            access_token: LinkedIn access token
            
        Returns:
            Dict containing profile information
            
        Raises:
            HTTPException: If profile retrieval fails
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            # Get basic profile
            profile_response = requests.get(LINKEDIN_PROFILE_URL, headers=headers)
            profile_response.raise_for_status()
            profile_data = profile_response.json()
            
            # Get email
            email_response = requests.get(LINKEDIN_EMAIL_URL, headers=headers)
            email_response.raise_for_status()
            email_data = email_response.json()
            
            # Get profile picture
            picture_response = requests.get(LINKEDIN_PROFILE_PICTURE_URL, headers=headers)
            picture_response.raise_for_status()
            picture_data = picture_response.json()
            
            # Extract email
            email = None
            if email_data.get("elements") and len(email_data["elements"]) > 0:
                email = email_data["elements"][0].get("handle~", {}).get("emailAddress")
            
            # Extract profile picture
            profile_picture = None
            if picture_data.get("profilePicture") and picture_data["profilePicture"].get("displayImage~"):
                elements = picture_data["profilePicture"]["displayImage~"].get("elements", [])
                if elements and len(elements) > 0:
                    for element in elements:
                        if element.get("data", {}).get("com.linkedin.digitalmedia.mediaartifact.StillImage"):
                            identifiers = element.get("identifiers", [])
                            if identifiers and len(identifiers) > 0:
                                profile_picture = identifiers[0].get("identifier")
                                break
            
            # Combine data
            combined_data = {
                "id": profile_data.get("id"),
                "firstName": profile_data.get("localizedFirstName"),
                "lastName": profile_data.get("localizedLastName"),
                "email": email,
                "profilePicture": profile_picture,
                "raw": {
                    "profile": profile_data,
                    "email": email_data,
                    "picture": picture_data
                }
            }
            
            return combined_data
        except requests.RequestException as e:
            logger.error(f"LinkedIn profile retrieval failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"LinkedIn profile retrieval failed: {str(e)}",
            )

    def search_jobs(
        self,
        access_token: str,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        experience_level: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Search for jobs on LinkedIn.
        
        Args:
            access_token: LinkedIn access token
            keywords: Job keywords to search for
            location: Location to search in
            job_type: Type of job (full-time, part-time, etc.)
            experience_level: Experience level required
            limit: Maximum number of results to return
            
        Returns:
            List of job results
            
        Raises:
            HTTPException: If job search fails
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Build query parameters
        params = {
            "count": limit,
        }
        
        if keywords:
            params["keywords"] = keywords
        
        if location:
            params["location"] = location
        
        # Note: LinkedIn API has specific parameters for job type and experience level
        # These would need to be mapped to LinkedIn's specific values
        
        try:
            response = requests.get(LINKEDIN_JOBS_URL, headers=headers, params=params)
            response.raise_for_status()
            jobs_data = response.json()
            
            # Process and return jobs
            jobs = []
            if jobs_data.get("elements"):
                for job in jobs_data["elements"]:
                    processed_job = {
                        "id": job.get("jobPosting", {}).get("id"),
                        "title": job.get("jobPosting", {}).get("title"),
                        "company": job.get("jobPosting", {}).get("companyDetails", {}).get("company", {}).get("name"),
                        "location": job.get("jobPosting", {}).get("formattedLocation"),
                        "description": job.get("jobPosting", {}).get("description", {}).get("text"),
                        "apply_url": job.get("jobPosting", {}).get("applyMethod", {}).get("companyApplyUrl"),
                        "posted_at": job.get("jobPosting", {}).get("listedAt"),
                        "raw": job
                    }
                    jobs.append(processed_job)
            
            return jobs
        except requests.RequestException as e:
            logger.error(f"LinkedIn job search failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"LinkedIn job search failed: {str(e)}",
            )


def get_linkedin_client() -> LinkedInClient:
    """
    Get a LinkedIn client instance.
    
    Returns:
        LinkedIn client instance
    """
    return LinkedInClient(
        client_id=settings.LINKEDIN_CLIENT_ID,
        client_secret=settings.LINKEDIN_CLIENT_SECRET,
        redirect_uri=settings.LINKEDIN_REDIRECT_URI,
    ) 