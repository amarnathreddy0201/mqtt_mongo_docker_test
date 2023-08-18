"""For handling exception."""
import logging

logger = logging.getLogger()
def log_errors(func):
    """For handling exception"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            logger.error(f"Error in {func.__name__}: {error}")
            raise  # re-throw the last exception
    return wrapper
