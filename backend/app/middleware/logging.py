"""
Structured logging with PII masking
"""
import logging
import re
from typing import Any, Dict


class PIIMaskingFormatter(logging.Formatter):
    """Formatter that masks PII in log messages"""
    
    # Patterns to mask
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_PATTERN = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with PII masking"""
        original = super().format(record)
        
        # Mask email addresses
        masked = re.sub(self.EMAIL_PATTERN, '[EMAIL_MASKED]', original)
        
        # Mask phone numbers
        masked = re.sub(self.PHONE_PATTERN, '[PHONE_MASKED]', masked)
        
        # Mask SSN
        masked = re.sub(self.SSN_PATTERN, '[SSN_MASKED]', masked)
        
        return masked


def setup_logging():
    """Configure logging with PII masking"""
    handler = logging.StreamHandler()
    handler.setFormatter(PIIMaskingFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger
