import logging
import os
import re
from logging.handlers import RotatingFileHandler
from starlette.middleware.base import BaseHTTPMiddleware, _StreamingResponse
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable
from core.config import settings


def ensure_log_directory_exists():
    """
    Ensure the log directory exists based on the application root.
    """
    log_dir = settings.LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def configure_logger(log_file_path: str, log_level: int) -> logging.Logger:
    """
    Set up a logger with rotating file handler.
    Args:
        log_file_path: Path to the log file.
        log_level: Logging level (INFO, ERROR, etc.)
    Returns:
        Configured logger instance.
    """
    handler = RotatingFileHandler(
        log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    
    logger = logging.getLogger(os.path.basename(log_file_path))
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logger


def redact_sensitive_info(data: str) -> str:
    """
    Redact sensitive information like passwords or tokens.
    Args:
        data: Input string to process.
    Returns:
        Redacted string.
    """
    patterns = [
        r'"password":\s*".+?"',
        r'"access_token":\s*".+?"',
    ]
    for pattern in patterns:
        data = re.sub(pattern, '"password":"[REDACTED]"', data)
        data = re.sub(pattern, '"access_token":"[REDACTED]"', data)
    return data


# Ensure logs directory is created
ensure_log_directory_exists()

# Initialize General & Error Loggers
general_logger = configure_logger(
    os.path.join(settings.LOG_DIR, "api_logs.log"), logging.INFO
)


error_logger = configure_logger(
    os.path.join(settings.LOG_DIR, "error_logs.log"), logging.ERROR
)


class APILogMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging requests and responses securely.
    Logs general requests and responses into one file and errors into another.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and response, and log securely.
        Args:
            request: HTTP Request
            call_next: Callable function for processing the request
        Returns:
            Response object
        """
        # Log request safely
        try:
            request_body = await request.body()
            safe_request_body = redact_sensitive_info(request_body.decode("utf-8"))
            general_logger.info(
                f"Incoming request: Method={request.method}, URL={request.url}, Headers={dict(request.headers)}, Body={safe_request_body}"
            )

            response = await call_next(request)

            # Handle streaming response
            if isinstance(response, _StreamingResponse):
                response_body = b""
                original_body_iterator = response.body_iterator

                # Collect the streaming content
                async def logging_body_iterator():
                    nonlocal response_body
                    async for chunk in original_body_iterator:
                        response_body += chunk
                        yield chunk

                response.body_iterator = logging_body_iterator()

                safe_response_body = redact_sensitive_info(
                    response_body.decode("utf-8")
                )

            else:
                # Handle standard responses
                response_body = response.body or b""
                safe_response_body = redact_sensitive_info(
                    response_body.decode("utf-8")
                )


            general_logger.info(
                f"Response: Status Code={response.status_code}, Headers={dict(response.headers)}, Body={safe_response_body}"
            )

            return response
        except Exception as e:
            # Log the exception safely
            error_logger.error(
                f"Exception occurred: {str(e)}, URL: {request.url}, Method: {request.method}"
            )
            raise
