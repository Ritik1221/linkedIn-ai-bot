"""
LLM client for the LinkedIn AI Agent.
This module provides functions for interacting with LLM models (Claude/GPT).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional, Union

import anthropic
import openai
from fastapi import HTTPException, status

from src.app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """LLM client for interacting with Claude/GPT models."""

    def __init__(
        self,
        provider: str = settings.LLM_PROVIDER,
        model: str = settings.LLM_MODEL,
        api_key: str = None,
    ):
        """
        Initialize the LLM client.
        
        Args:
            provider: LLM provider (anthropic, openai)
            model: LLM model name
            api_key: API key for the provider
        """
        self.provider = provider.lower()
        self.model = model
        
        if self.provider == "anthropic":
            self.api_key = api_key or settings.ANTHROPIC_API_KEY
            self.client = anthropic.Anthropic(api_key=self.api_key)
        elif self.provider == "openai":
            self.api_key = api_key or settings.OPENAI_API_KEY
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
            
        Raises:
            HTTPException: If text generation fails
        """
        try:
            if self.provider == "anthropic":
                return self._generate_text_anthropic(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            elif self.provider == "openai":
                return self._generate_text_openai(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
        except Exception as e:
            logger.error(f"LLM text generation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"LLM text generation failed: {str(e)}",
            )

    def _generate_text_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using Anthropic Claude.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        messages = [{"role": "user", "content": prompt}]
        
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            system=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        return response.content[0].text

    def _generate_text_openai(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using OpenAI GPT.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        return response.choices[0].message.content

    def analyze_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a LinkedIn profile using LLM.
        
        Args:
            profile_data: LinkedIn profile data
            
        Returns:
            Analysis results
        """
        # Create a prompt for profile analysis
        prompt = f"""
        Analyze the following LinkedIn profile and provide:
        1. Key strengths
        2. Areas for improvement
        3. Specific recommendations to enhance the profile
        4. Skills assessment
        
        Profile data:
        {json.dumps(profile_data, indent=2)}
        
        Format your response as JSON with the following structure:
        {{
            "strengths": ["strength1", "strength2", ...],
            "weaknesses": ["weakness1", "weakness2", ...],
            "recommendations": ["recommendation1", "recommendation2", ...],
            "skills_assessment": {{
                "present": ["skill1", "skill2", ...],
                "missing": ["skill1", "skill2", ...],
                "recommendations": ["recommendation1", "recommendation2", ...]
            }}
        }}
        """
        
        system_prompt = "You are an expert LinkedIn profile analyzer. Provide detailed, professional analysis of LinkedIn profiles."
        
        response = self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2000,
            temperature=0.3,
        )
        
        try:
            # Parse the JSON response
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured response
            logger.error("Failed to parse LLM response as JSON")
            return {
                "strengths": ["Could not parse strengths"],
                "weaknesses": ["Could not parse weaknesses"],
                "recommendations": ["Could not parse recommendations"],
                "skills_assessment": {
                    "present": [],
                    "missing": [],
                    "recommendations": ["Could not parse skills assessment"]
                },
                "raw_response": response
            }

    def match_job(
        self, profile_data: Dict[str, Any], job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Match a job to a user's profile using LLM.
        
        Args:
            profile_data: LinkedIn profile data
            job_data: Job data
            
        Returns:
            Match results
        """
        # Create a prompt for job matching
        prompt = f"""
        Analyze the following LinkedIn profile and job posting to determine:
        1. Overall match score (0-100)
        2. Key matching skills and experiences
        3. Missing skills or experiences
        4. Recommendations for the candidate
        
        Profile data:
        {json.dumps(profile_data, indent=2)}
        
        Job posting:
        {json.dumps(job_data, indent=2)}
        
        Format your response as JSON with the following structure:
        {{
            "match_score": 85,
            "matching_points": ["point1", "point2", ...],
            "missing_points": ["point1", "point2", ...],
            "recommendations": ["recommendation1", "recommendation2", ...],
            "summary": "A brief summary of the match analysis"
        }}
        """
        
        system_prompt = "You are an expert job matcher. Provide detailed, professional analysis of how well a candidate matches a job posting."
        
        response = self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2000,
            temperature=0.3,
        )
        
        try:
            # Parse the JSON response
            match_results = json.loads(response)
            return match_results
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured response
            logger.error("Failed to parse LLM response as JSON")
            return {
                "match_score": 50,
                "matching_points": ["Could not parse matching points"],
                "missing_points": ["Could not parse missing points"],
                "recommendations": ["Could not parse recommendations"],
                "summary": "Could not generate a proper match analysis",
                "raw_response": response
            }

    def generate_cover_letter(
        self,
        profile_data: Dict[str, Any],
        job_data: Dict[str, Any],
        customization_notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a cover letter for a job application using LLM.
        
        Args:
            profile_data: LinkedIn profile data
            job_data: Job data
            customization_notes: Additional notes for customization
            
        Returns:
            Generated cover letter
        """
        # Create a prompt for cover letter generation
        prompt = f"""
        Generate a professional cover letter for a job application based on the following:
        
        Profile data:
        {json.dumps(profile_data, indent=2)}
        
        Job posting:
        {json.dumps(job_data, indent=2)}
        """
        
        if customization_notes:
            prompt += f"\nAdditional customization notes:\n{customization_notes}"
        
        prompt += """
        
        Format your response as JSON with the following structure:
        {
            "subject_line": "Subject line for the application email",
            "salutation": "Dear Hiring Manager,",
            "introduction": "First paragraph introducing the candidate and position",
            "body": "Main paragraphs highlighting relevant experience and skills",
            "closing": "Closing paragraph with call to action",
            "signature": "Sincerely,\\n[Candidate Name]",
            "full_text": "The complete cover letter text"
        }
        """
        
        system_prompt = "You are an expert cover letter writer. Create personalized, compelling cover letters that highlight relevant skills and experiences."
        
        response = self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2000,
            temperature=0.7,
        )
        
        try:
            # Parse the JSON response
            cover_letter = json.loads(response)
            return cover_letter
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured response
            logger.error("Failed to parse LLM response as JSON")
            return {
                "subject_line": "Application for [Job Title]",
                "salutation": "Dear Hiring Manager,",
                "introduction": "Could not generate introduction",
                "body": "Could not generate body",
                "closing": "Could not generate closing",
                "signature": "Sincerely,\n[Candidate Name]",
                "full_text": response
            }


def get_llm_client() -> LLMClient:
    """
    Get an LLM client instance.
    
    Returns:
        LLM client instance
    """
    return LLMClient(
        provider=settings.LLM_PROVIDER,
        model=settings.LLM_MODEL,
    ) 