from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SneakerCategory = Literal["Basketball", "Football", "Lifestyle", "Running"]


class Sneaker(BaseModel):
    """Validated representation of one sneaker in the catalog."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: int = Field(gt=0)
    brand: str = Field(min_length=2, max_length=50)
    model: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1900, le=2100)
    colorway: str = Field(min_length=2, max_length=120)
    price: str = Field(pattern=r"^₱[\d,]+$")
    description: str = Field(min_length=10, max_length=300)
    category: SneakerCategory
    materials: list[str] = Field(min_length=1, max_length=6)
    country_of_origin: str = Field(min_length=2, max_length=50)


class SneakerCollection(BaseModel):
    count: int = Field(ge=0)
    sneakers: list[Sneaker]


class SneakerSearchResults(BaseModel):
    query: str
    count: int = Field(ge=0)
    results: list[Sneaker]


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    timestamp: str
