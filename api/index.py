from datetime import datetime, timezone

from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from api.auth import verify_api_key
from api.data import SNEAKER_CATALOG
from api.models import (
    HealthResponse,
    Sneaker,
    SneakerCollection,
    SneakerSearchResults,
)
from api.services import find_sneaker, search_catalog


app = FastAPI(
    title="SOLE Sneaker API",
    description="A validated sneaker catalog with public and protected endpoints.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Content-Type", "x-api-key"],
)


def collection_response() -> SneakerCollection:
    return SneakerCollection(count=len(SNEAKER_CATALOG), sneakers=SNEAKER_CATALOG)


def search_response(query: str) -> SneakerSearchResults:
    results = search_catalog(SNEAKER_CATALOG, query)
    return SneakerSearchResults(query=query, count=len(results), results=results)


@app.get("/", tags=["Service"])
def home() -> dict[str, str | list[str]]:
    return {
        "message": "Welcome to the SOLE Sneaker API!",
        "documentation": "/docs",
        "public_endpoints": ["/health", "/sneakers", "/sneakers/search"],
        "protected_endpoints": ["/api/v1/sneakers", "/api/v1/sneakers/search"],
    }


@app.get("/health", response_model=HealthResponse, tags=["Service"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="SOLE Sneaker API",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# Public read-only routes used by the static website. No secret is sent to app.js.
@app.get("/sneakers", response_model=SneakerCollection, tags=["Public catalog"])
def get_public_sneakers() -> SneakerCollection:
    return collection_response()


@app.get(
    "/sneakers/search",
    response_model=SneakerSearchResults,
    tags=["Public catalog"],
)
def search_public_sneakers(
    q: str = Query(min_length=1, max_length=100),
) -> SneakerSearchResults:
    return search_response(q)


@app.get("/sneakers/{sneaker_id}", response_model=Sneaker, tags=["Public catalog"])
def get_public_sneaker(sneaker_id: int) -> Sneaker:
    return find_sneaker(SNEAKER_CATALOG, sneaker_id)


# Course requirement: every v1 route requires the x-api-key request header.
protected_router = APIRouter(
    prefix="/api/v1",
    tags=["Protected catalog"],
    dependencies=[Depends(verify_api_key)],
)


@protected_router.get("/sneakers", response_model=SneakerCollection)
def get_protected_sneakers() -> SneakerCollection:
    return collection_response()


@protected_router.get("/sneakers/search", response_model=SneakerSearchResults)
def search_protected_sneakers(
    q: str = Query(min_length=1, max_length=100),
) -> SneakerSearchResults:
    return search_response(q)


@protected_router.get("/sneakers/{sneaker_id}", response_model=Sneaker)
def get_protected_sneaker(sneaker_id: int) -> Sneaker:
    return find_sneaker(SNEAKER_CATALOG, sneaker_id)


app.include_router(protected_router)
