# SOLE Sneaker API and Finder

SOLE is a static sneaker browser backed by a FastAPI catalog. The public,
read-only endpoints power the website. The versioned `/api/v1` endpoints use an
API key for coursework authentication checks.

## Project structure

```text
api/
  auth.py       API-key verification
  data.py       sneaker dataset and startup validation
  index.py      FastAPI app and routes
  models.py     Pydantic request/response schemas
  services.py   reusable lookup and search logic
images/         hero and sneaker images
tests/          API behavior tests
app.js          browser behavior
index.html      page structure
style.css       page design
```

## Run locally

Create and activate a Python virtual environment, then install the development
dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Set a local-only key and start the API:

```powershell
$env:SNEAKER_API_KEY = "class-demo-key"
uvicorn api.index:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation. Run the
tests with `pytest -q`.

## Screenshot checklist

1. **Schema:** open `api/models.py` and show the complete `Sneaker` class,
   including `BaseModel`, `Field`, and `Literal`.
2. **Startup validation:** open the bottom of `api/data.py` and show
   `validated_sneakers = [Sneaker(**sneaker).model_dump() ...]` directly below
   the dataset.
3. **Authentication:** show `verify_api_key` in `api/auth.py` beside the
   `dependencies=[Depends(verify_api_key)]` router in `api/index.py`.
4. **Health output:** open `http://127.0.0.1:8000/health`.
5. **Unauthorized output:** open `http://127.0.0.1:8000/api/v1/sneakers`
   without a key and capture the `401` response in the browser network panel or
   an API client.
6. **Metadata search:** in `/docs`, authorize with `class-demo-key`, then call
   `/api/v1/sneakers/search?q=China` and capture the successful Anta results.
7. **GitHub:** after committing and pushing, capture the repository commit log.
8. **Vercel:** set `SNEAKER_API_KEY` in Vercel, deploy, and capture the green
   deployment status beside the live `/health` or `/docs` page.

Never put the real API key in `app.js`, commit it, or include it in a screenshot.
