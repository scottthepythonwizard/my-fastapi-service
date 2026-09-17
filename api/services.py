from fastapi import HTTPException, status

from api.models import Sneaker


def find_sneaker(sneakers: list[Sneaker], sneaker_id: int) -> Sneaker:
    sneaker = next((item for item in sneakers if item.id == sneaker_id), None)
    if sneaker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sneaker not found.",
        )
    return sneaker


def search_catalog(sneakers: list[Sneaker], query: str) -> list[Sneaker]:
    normalized_query = query.casefold().strip()

    return [
        sneaker
        for sneaker in sneakers
        if normalized_query
        in " ".join(
            [
                sneaker.brand,
                sneaker.model,
                str(sneaker.year),
                sneaker.colorway,
                sneaker.description,
                sneaker.category,
                *sneaker.materials,
                sneaker.country_of_origin,
            ]
        ).casefold()
    ]
