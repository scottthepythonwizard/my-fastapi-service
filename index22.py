from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Simple Sneaker API",
    description="A beginner-friendly REST API containing information about Sneakers.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SNEAKERS DATA
sneakers = [

    {
        "id": 1,
        "brand": "Nike",
        "model": "Air Jordan 1 Retro High OG",
        "year": 1985,
        "colorway": "Chicago (White/Black/Red)",
        "price": "₱13,000",
        "description": "The sneaker that launched the Jordan line."
    },

    {
        "id": 2,
        "brand": "Adidas",
        "model": "Yeezy Boost 350 V2",
        "year": 2016,
        "colorway": "Zebra (White/Black)",
        "price": "₱12,000",
        "description": "A Kanye West collaboration."
    },

    {
        "id": 3,
        "brand": "Nike",
        "model": "Air Force 1 Low",
        "year": 1982,
        "colorway": "Triple White",
        "price": "₱7,000",
        "description": "An all-white low-top classic and one of the best-selling sneakers of all time."
    },

    {
        "id": 4,
        "brand": "New Balance",
        "model": "550",
        "year": 1989,
        "colorway": "White/Green",
        "price": "₱130",
        "description": "A retro basketball silhouette that became a streetwear staple."
    },

    {
        "id": 5,
        "brand": "Converse",
        "model": "Chuck Taylor All Star",
        "year": 1922,
        "colorway": "Black & White",
        "price": "₱6,000",
        "description": "One of the most recognizable sneakers ever made."
    },

    {
        "id": 6,
        "brand": "Adidas",
        "model": "Adidas Adizero EVO SL",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 7,
        "brand": "Nike",
        "model": "Nike Kobe 5",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 8,
        "brand": "Adidas",
        "model": "Adidas F50 Hyperfast Elite",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },
    
    {
        "id": 9,
        "brand": "New Balance",
        "model": "Furon V8 Elite FG",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 10,
        "brand": "Jordan",
        "model": "Jordan 4",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 11,
        "brand": "Nike",
        "model": "Nike Mercurial Superfly 9 Elite",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 12,
        "brand": "Adidas",
        "model": "adidas Harden Volume 10",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },
    
    {
        "id": 13,
        "brand": "New Balance",
        "model": "New Balance Fresh Foam BB v3",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 14,
        "brand": "Nike",
        "model": "G.T Cut 1",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 15,
        "brand": "Nike",
        "model": "Nike V2K Run",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 16,
        "brand": "Puma",
        "model": "Speedcat",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },
    
    {
        "id": 17,
        "brand": "Onitsuka Tiger",
        "model": "Mexico 66",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 18,
        "brand": "New Balance",
        "model": "New Balance Tekela V5 Elite FG",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 19,
        "brand": "Anta",
        "model": "Shock Wave 8",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    },

    {
        "id": 20,
        "brand": "Anta",
        "model": "Rocket 6",
        "year": 99,
        "colorway": "",
        "price": "₱6,000",
        "description": ""
    }

]

# HOME
@app.get("/")
def home():

    return {
        "message": "Welcome to the Simple Sneaker API!",
        "endpoints": [
            "/sneakers",
            "/sneakers/{id}",
            "/sneakers/search"
        ]
    }


# GET ALL sneakers
@app.get("/sneakers")
def get_sneakers():

    return {
        "count": len(sneakers),
        "sneakers": sneakers
    }


# GET ONE sneaker
@app.get("/sneakers/{sneaker_id}")
def get_sneaker(sneaker_id: int):

    for sneaker in sneakers:

        if sneaker["id"] == sneaker_id:
            return sneaker

    raise HTTPException(
        status_code=404,
        detail="sneaker not found."
    )

# SEARCH sneakers
@app.get("/sneakers/search")
def search_sneakers( q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []
    for sneaker in sneakers:
        searchable_text = (
            f"{sneaker['brand']} "
            f"{sneaker['model']} "
            f"{sneaker['year']} "
            f"{sneaker['colorway']}"
        ).lower()

        if q in searchable_text:
            results.append(sneaker)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }

