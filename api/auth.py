import os
import secrets

from fastapi import Header, HTTPException, status


API_KEY_ENV_NAME = "SNEAKER_API_KEY"


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Require the API key configured on the server for protected routes."""

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    expected_api_key = os.getenv(API_KEY_ENV_NAME)
    if not expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Server API key is not configured ({API_KEY_ENV_NAME}).",
        )

    if not secrets.compare_digest(x_api_key, expected_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
