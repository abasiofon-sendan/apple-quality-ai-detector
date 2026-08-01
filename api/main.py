## `api/main.py`


"""
===============================================================================
AppleGuard AI — FastAPI Application
===============================================================================

Project      : AppleGuard AI
Module       : api.main
Author       : Group 16

Purpose
-------
Main FastAPI backend entry point.

Responsibilities
----------------
• Create FastAPI application
• Configure API metadata
• Register middleware
• Register API routes
• Manage startup/shutdown lifecycle
• Handle global exceptions
• Provide root and health endpoints

Run
---
uvicorn api.main:app --reload
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# IMPORTS
# =============================================================================
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import router as api_router
from src.config import (
    API_DESCRIPTION,
    API_HOST,
    API_PORT,
    API_TITLE,
    API_VERSION,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_HEADERS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_ORIGINS,
    PROJECT_NAME,
)
from src.helpers import (
    print_error,
    print_info,
    print_success,
)
from src import predict

# Keep startup compatible with predict modules that do not expose optional
# model validation yet.
validate_models = getattr(predict, "validate_models", lambda: None)

# =============================================================================
# APPLICATION LIFESPAN
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle manager.
    """

    print("=" * 78)
    print(f"Starting {PROJECT_NAME} API...")
    print("=" * 78)

    try:
        validate_models()

        print_success("All registered models validated successfully.")

        print_info(f"API Title   : {API_TITLE}")
        print_info(f"API Version : {API_VERSION}")

    except Exception as error:
        print_error(f"Model validation failed: {error}")

    # Startup complete
    yield

    # Shutdown
    print("=" * 78)
    print(f"Shutting down {PROJECT_NAME} API...")
    print("=" * 78)

# =============================================================================
# CREATE FASTAPI APPLICATION
# =============================================================================

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# =============================================================================
# CORS MIDDLEWARE
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# =============================================================================
# GLOBAL EXCEPTION HANDLERS
# =============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """
    Handle FastAPI request validation errors.
    """

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "validation_error",
            "message": "Request validation failed.",
            "details": exc.errors(),
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected server errors.
    """

    print_error(f"Unhandled exception: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "internal_server_error",
            "message": "An unexpected server error occurred.",
        },
    )

# =============================================================================
# REGISTER API ROUTES
# =============================================================================

app.include_router(api_router)

# =============================================================================
# ROOT ENDPOINT
# =============================================================================

@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
)
async def root():
    """
    API root endpoint.
    """

    return {
        "project": PROJECT_NAME,
        "version": API_VERSION,
        "status": "running",
        "documentation": "/docs",
        "redoc": "/redoc",
    }

# =============================================================================
# HEALTH CHECK ENDPOINT
# =============================================================================

@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
)
async def health_check():
    """
    Lightweight health check endpoint.
    """

    return {
        "success": True,
        "service": PROJECT_NAME,
        "status": "healthy",
        "version": API_VERSION,
    }

# =============================================================================
# MODULE TEST / DEVELOPMENT ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    print("=" * 78)
    print(f"{PROJECT_NAME} — FastAPI Application")
    print("=" * 78)

    print(f"Title   : {API_TITLE}")
    print(f"Version : {API_VERSION}")
    print(f"Host    : {API_HOST}")
    print(f"Port    : {API_PORT}")
    print("Router  : Registered")
    print("Status  : Ready")

    print("=" * 78)

    uvicorn.run(
        "api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
    )

