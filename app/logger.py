import logging
import sys
from app.config import Config

def setup_logger():
    """Configures a standardized structured logger for the application."""
    logger = logging.getLogger("emotion_agent")
    logger.setLevel(Config.LOG_LEVEL)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Stream handler for console/Colab output
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
    return logger

logger = setup_logger()