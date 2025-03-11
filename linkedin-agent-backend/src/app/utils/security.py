"""
Security utilities for the LinkedIn AI Agent.
This module provides security-related utilities like PII masking.
"""

import logging
import re
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


def mask_pii(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mask personally identifiable information (PII) in a dictionary.
    
    Args:
        data: Dictionary containing potentially sensitive data
        
    Returns:
        Dictionary with PII masked
    """
    # Create a copy to avoid modifying the original
    masked_data = data.copy()
    
    # Mask email
    if "email" in masked_data and masked_data["email"]:
        try:
            name, domain = masked_data["email"].split("@")
            if len(name) > 2:
                masked_data["email"] = f"{name[0]}{'*' * (len(name) - 2)}{name[-1]}@{domain}"
            else:
                masked_data["email"] = f"{'*' * len(name)}@{domain}"
        except Exception as e:
            logger.warning(f"Failed to mask email: {str(e)}")
    
    # Mask phone number
    if "phone" in masked_data and masked_data["phone"]:
        try:
            # Remove any non-digit characters for consistent handling
            digits = re.sub(r'\D', '', masked_data["phone"])
            if len(digits) >= 4:
                masked_data["phone"] = f"{'*' * (len(digits) - 4)}{digits[-4:]}"
            else:
                masked_data["phone"] = '*' * len(digits)
        except Exception as e:
            logger.warning(f"Failed to mask phone: {str(e)}")
    
    # Mask physical address
    if "address" in masked_data and masked_data["address"]:
        try:
            # Simple approach: keep first line of address but mask house/apartment number
            address_lines = masked_data["address"].split('\n')
            first_line = address_lines[0]
            
            # Try to mask house/apartment number at beginning of address
            words = first_line.split()
            if words and words[0].isdigit():
                words[0] = '*' * len(words[0])
                address_lines[0] = ' '.join(words)
                
            masked_data["address"] = '\n'.join(address_lines)
        except Exception as e:
            logger.warning(f"Failed to mask address: {str(e)}")
    
    # Mask social security number or other ID numbers
    for key in ["ssn", "social_security", "tax_id", "passport_number", "id_number"]:
        if key in masked_data and masked_data[key]:
            try:
                digits = re.sub(r'\D', '', masked_data[key])
                if len(digits) >= 4:
                    masked_data[key] = f"{'*' * (len(digits) - 4)}{digits[-4:]}"
                else:
                    masked_data[key] = '*' * len(digits)
            except Exception as e:
                logger.warning(f"Failed to mask {key}: {str(e)}")
    
    # Mask dates (birthdate, etc.)
    if "birthdate" in masked_data and masked_data["birthdate"]:
        try:
            # Only keep year, mask month and day
            date_str = str(masked_data["birthdate"])
            if len(date_str) >= 4 and '-' in date_str:
                parts = date_str.split('-')
                if len(parts) == 3:
                    # Assuming YYYY-MM-DD format
                    masked_data["birthdate"] = f"{parts[0]}-**-**"
                else:
                    masked_data["birthdate"] = "****-**-**"
        except Exception as e:
            logger.warning(f"Failed to mask birthdate: {str(e)}")
    
    # Process nested dictionaries
    for key, value in masked_data.items():
        if isinstance(value, dict):
            masked_data[key] = mask_pii(value)
        elif isinstance(value, list):
            # Process lists of dictionaries
            masked_data[key] = [
                mask_pii(item) if isinstance(item, dict) else item
                for item in value
            ]
    
    return masked_data


def mask_sensitive_logs(log_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mask sensitive information in log data.
    
    Args:
        log_data: Log data dictionary
        
    Returns:
        Dictionary with sensitive information masked
    """
    sensitive_keys = [
        "password", "token", "access_token", "refresh_token", "api_key", 
        "secret", "authorization", "credit_card", "card_number"
    ]
    
    # Create a copy to avoid modifying the original
    masked_logs = log_data.copy()
    
    # Mask sensitive keys
    for key in masked_logs:
        if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
            if isinstance(masked_logs[key], str):
                masked_logs[key] = "********"
    
    return masked_logs 