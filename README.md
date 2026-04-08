[![GitHub license](https://img.shields.io/github/license/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/issues)
[![GitHub stars](https://img.shields.io/github/stars/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/stargazers)
[![Tests](https://github.com/wkambale/Ug-Universities-Api/actions/workflows/test.yml/badge.svg)](https://github.com/wkambale/Ug-Universities-Api/actions/workflows/test.yml)

# Uganda Universities API

A REST API listing universities in Uganda with geographic, domain, and classification data. Built with **FastAPI**, backed by **PostgreSQL** (Cloud SQL), containerized with **Docker**, and deployed to **Google Cloud Run**.

## Features

- 🏫 **47 universities** — public and private institutions across Uganda
- 🌍 **Geo data** — latitude/longitude coordinates for map rendering
- 🔍 **Search & filter** — by name, location, type, with full-text search
- 📄 **Pagination** — configurable page size, ordering, and cursor links
- 📊 **Stats** — aggregate counts by type and location
- 📥 **Export** — download full dataset as JSON or CSV
- 🔒 **Admin routes** — bearer token-protected write endpoints
- 📘 **OpenAPI docs** — auto-generated Swagger UI and ReDoc

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.111+ (async) |
| ORM | SQLAlchemy 2.0 (async) + Alembic |
| Database | PostgreSQL 15 (Cloud SQL) |
| Schemas | Pydantic v2 |
| Container | Docker (Python 3.12-slim) |
| Deployment | Google Cloud Run (`africa-south1`) |
| CI/CD | GitHub Actions |

## API Endpoints

### Public (read)

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/v1/universities/` | List all (paginated, filterable) |
| `GET` | `/api/v1/universities/{id}` | Single university by ID |
| `GET` | `/api/v1/universities/geo` | Coordinates for map rendering |
| `GET` | `/api/v1/universities/domains` | All registered domains |
| `GET` | `/api/v1/universities/locations` | Distinct locations |
| `GET` | `/api/v1/universities/types` | Valid type values |
| `GET` | `/api/v1/universities/count` | Count by type |
| `GET` | `/api/v1/universities/export/json` | Full dataset as JSON |
| `GET` | `/api/v1/universities/export/csv` | Full dataset as CSV |
| `GET` | `/api/v1/stats/` | Aggregate statistics |
| `GET` | `/health` | Liveness check |
| `GET` | `/ready` | Readiness check (DB) |

### Admin (bearer token required)

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/v1/universities/` | Create university |
| `PUT` | `/api/v1/universities/{id}` | Full update |
| `PATCH` | `/api/v1/universities/{id}` | Partial update |
| `DELETE` | `/api/v1/universities/{id}` | Soft-delete |

### Query Parameters

```
?type=public           Filter by type (public, private, military)
?location=Kampala      Filter by location (partial match)
?search=makerere       Search name, abbrev, location
?is_active=true        Show active (default) or inactive
?ordering=-established Sort field (prefix - for descending)
?page=2&page_size=50   Pagination (default 20, max 100)
```

## Local Development

### Prerequisites

- Python 3.12+
- PostgreSQL 15+ (or use SQLite for quick testing)

### Setup

```bash
# Clone and enter the project
git clone https://github.com/wkambale/Ug-Universities-Api.git
cd Ug-Universities-Api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Create .env from template
cp .env.example .env
# Edit .env with your local database credentials

# Run the API
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `/docs` for interactive Swagger UI.

### Run Tests

```bash
pytest tests/ -v
```

Tests use an in-memory SQLite database — no PostgreSQL required.

### Lint

```bash
ruff check app/
```

### Docker

```bash
docker build -t ug-universities-api .
docker run -p 8080:8080 --env-file .env ug-universities-api
```

## Data

The source data is in `uganda-universities-domains.json`. Each entry includes:

```json
{
  "name": "Makerere University",
  "abbrev": "MAK",
  "location": "Makerere",
  "type": "public",
  "established": 1922,
  "latitude": 0.33375,
  "longitude": 32.56752,
  "domains": ["mak.ac.ug"],
  "web_pages": ["http://www.mak.ac.ug/"],
  "alpha_two_code": "UG",
  "alpha_three_code": "UGA",
  "country": "Uganda"
}
```

### Seed the Database

```bash
python scripts/seed.py
```

## Contributing

Pull requests are welcome. Do not hesitate to fix any wrong data. But please open an issue first to discuss what you would like to change.

- Check out [CONTRIBUTING.md](CONTRIBUTING.md) for information about getting involved.

## License

[MIT License](https://github.com/WesleyKambale/Ug-Universities-Api/blob/main/LICENSE)

## Creation

Created by [Wesley Kambale](https://kambale.dev)
