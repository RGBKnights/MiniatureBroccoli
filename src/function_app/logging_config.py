import os
import logging
import json
from opencensus.ext.azure.log_exporter import AzureLogHandler

def setup_logging():
    """
    Configure logging with Azure Application Insights
    """
    # Get the instrumentation key from environment variables
    instrumentation_key = os.environ.get('APPINSIGHTS_INSTRUMENTATIONKEY', '')
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Add Azure App Insights handler if instrumentation key is available
    if instrumentation_key:
        azure_handler = AzureLogHandler(connection_string=f'InstrumentationKey={instrumentation_key}')
        azure_handler.setLevel(logging.INFO)
        root_logger.addHandler(azure_handler)
        logging.info("Azure Application Insights logging enabled")
    else:
        logging.info("Azure Application Insights instrumentation key not found, using console logging only")
    
    # Return the configured logger
    return root_logger

def log_request(logger, req):
    """
    Log details about the incoming request
    """
    headers = dict(req.headers)
    # Remove sensitive headers
    if 'Authorization' in headers:
        headers['Authorization'] = '[REDACTED]'
    
    request_data = {
        'url': req.url,
        'method': req.method,
        'headers': headers,
        'params': dict(req.params),
    }
    
    logger.info(f"Request received: {json.dumps(request_data)}")