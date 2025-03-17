# Azure Function app initialization
import logging
from .logging_config import setup_logging

# Set up logging when the module is imported
logger = setup_logging()
logging.info("Azure Function app initialized")