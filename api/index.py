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
            "price": "₱6,500",
            "description": "A retro basketball silhouette that became a streetwear staple."
        },

        {
            "id": 5,
            "brand": "Converse",
            "model": "Chuck Taylor All Star",
            "year": 1922,
            "colorway": "Black & White",
            "price": "₱4,000",
            "description": "One of the most recognizable sneakers ever made."
        },

        {
            "id": 6,
            "brand": "Adidas",
            "model": "Adidas Adizero EVO SL",
            "year": 2024,
            "colorway": "White / Core Black",
            "price": "₱9,000",
            "description": "A lightweight daily trainer inspired by Adidas' elite race-day super shoes."
        },

        {
            "id": 7,
            "brand": "Nike",
            "model": "Nike Kobe 5",
            "year": 2009,
            "colorway": "Bruce Lee (Del Sol/Black)",
            "price": "₱9,895",
            "description": "Low-top basketball shoe famous for its extreme lightweight support and low court feel."
        },

        {
            "id": 8,
            "brand": "Adidas",
            "model": "Adidas F50 Elite FG",
            "year": 2024,
            "colorway": "Advancement Pack (White/Solar Red/Lucid Blue)",
            "price": "₱14,500",
            "description": "High-performance football boot engineered for lightweight speed and acceleration."
        },

        {
            "id": 9,
            "brand": "New Balance",
            "model": "Furon V7 Elite FG",
            "year": 2024,
            "colorway": "Dragonfruit / Black",
            "price": "₱12,500",
            "description": "Elite speed boot featuring a minimal Hypoknit upper and responsive outsole."
        },

        {
            "id": 10,
            "brand": "Jordan",
            "model": "Air Jordan 4",
            "year": 1989,
            "colorway": "White Cement",
            "price": "₱11,500",
            "description": "Tinker Hatfield design featuring mesh side panels and iconic support wings."
        },

        {
            "id": 11,
            "brand": "Jordan",
            "model": "Air Jordan 3",
            "year": 1988,
            "colorway": "Black Cement (Black/Fire Red-Cement Grey)",
            "price": "₱12,000",
            "description": "Iconic Tinker Hatfield silhouette that introduced the Jumpman logo and legendary elephant print overlays."
        },

        {
            "id": 12,
            "brand": "Adidas",
            "model": "Adidas Harden Volume 8",
            "year": 2024,
            "colorway": "Pioneer (Core Black/Cloud White)",
            "price": "₱8,900",
            "description": "James Harden signature basketball shoe with a distinctive EVA cage and Jet Boost midsole."
        },

        {
            "id": 13,
            "brand": "New Balance",
            "model": "New Balance Fresh Foam BB v2",
            "year": 2024,
            "colorway": "Moon Daze / Sea Salt",
            "price": "₱8,250",
            "description": "Dual-density Fresh Foam X basketball shoe built for cushioned impact protection."
        },

        {
            "id": 14,
            "brand": "Converse",
            "model": "Chuck 70 CDG Play Low",
            "year": 2015,
            "colorway": "Black / White / High Risk Red",
            "price": "₱8,500",
            "description": "A premium Chuck 70 elevated by the iconic bug-eyed heart logo from COMME des GARÇONS PLAY."
        },

        {
            "id": 15,
            "brand": "Nike",
            "model": "Nike V2K Run",
            "year": 2023,
            "colorway": "Summit White / Metallic Silver",
            "price": "₱6,895",
            "description": "Retro Y2K running silhouette combining metallic accents and dual-density foam."
        },

        {
            "id": 16,
            "brand": "Puma",
            "model": "Speedcat",
            "year": 1999,
            "colorway": "Black / White",
            "price": "₱5,500",
            "description": "Motorsport-inspired low-profile classic originally created for Formula 1 drivers."
        },

        {
            "id": 17,
            "brand": "Onitsuka Tiger",
            "model": "Mexico 66",
            "year": 1966,
            "colorway": "Birch / Peacoat",
            "price": "₱7,000",
            "description": "Iconic vintage lifestyle sneaker featuring the signature stripe design."
        },

        {
            "id": 18,
            "brand": "New Balance",
            "model": "New Balance Tekela V4 Elite FG",
            "year": 2024,
            "colorway": "Metallic Gold / Black",
            "price": "₱12,500",
            "description": "Laceless football boot created for playmakers seeking touch and multidirectional traction."
        },

        {
            "id": 19,
            "brand": "Anta",
            "model": "Shock Wave 5",
            "year": 2023,
            "colorway": "Kyrie Irving / Salt",
            "price": "₱6,500",
            "description": "Durable high-traction outdoor basketball sneaker endorsed by Kyrie Irving."
        },

        {
            "id": 20,
            "brand": "Anta",
            "model": "Rocket 6",
            "year": 2023,
            "colorway": "White / Red",
            "price": "₱4,500",
            "description": "Budget-friendly performance basketball shoe focused on stability and court grip."
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

