import pytest


@pytest.mark.asyncio
async def test_health(client):
    """Liveness check — always returns 200 if container is up."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_ready(client):
    """Readiness check — returns 200 when DB is reachable."""
    response = await client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


@pytest.mark.asyncio
async def test_root(client):
    """Root endpoint returns API metadata and links."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Uganda Universities API"
    assert data["version"] == "2.0.0"
    assert data["docs"] == "/docs"
    assert data["redoc"] == "/redoc"
    assert data["universities"] == "/api/v1/universities/"
    assert data["stats"] == "/api/v1/stats/"


@pytest.mark.asyncio
async def test_docs_available(client):
    """OpenAPI docs should be available at /docs."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_openapi_schema(client):
    """OpenAPI JSON schema should be available."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Uganda Universities API"
    assert schema["info"]["version"] == "2.0.0"


@pytest.mark.asyncio
async def test_geo_endpoint(client, admin_headers):
    """Geo endpoint returns universities with coordinates."""
    await client.post("/api/v1/universities/", json={
        "name": "Geo Uni", "location": "Kampala", "type": "public",
        "domains": [], "web_pages": [],
        "latitude": 0.3476, "longitude": 32.5825
    }, headers=admin_headers)

    response = await client.get("/api/v1/universities/geo")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["latitude"] == 0.3476
    assert data[0]["longitude"] == 32.5825


@pytest.mark.asyncio
async def test_domains_endpoint(client, admin_headers):
    """Domains endpoint returns flat list of all domains."""
    await client.post("/api/v1/universities/", json={
        "name": "Domain Uni", "location": "Kampala", "type": "public",
        "domains": ["mak.ac.ug", "mak.edu"], "web_pages": []
    }, headers=admin_headers)

    response = await client.get("/api/v1/universities/domains")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "mak.ac.ug" in data
    assert "mak.edu" in data


@pytest.mark.asyncio
async def test_locations_endpoint(client, admin_headers):
    """Locations endpoint returns distinct list of locations."""
    await client.post("/api/v1/universities/", json={
        "name": "Loc Uni 1", "location": "Kampala", "type": "public", "domains": [], "web_pages": []
    }, headers=admin_headers)
    await client.post("/api/v1/universities/", json={
        "name": "Loc Uni 2", "location": "Gulu", "type": "private", "domains": [], "web_pages": []
    }, headers=admin_headers)

    response = await client.get("/api/v1/universities/locations")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "Kampala" in data
    assert "Gulu" in data


@pytest.mark.asyncio
async def test_types_endpoint(client):
    """Types endpoint returns valid university type enum values."""
    response = await client.get("/api/v1/universities/types")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "public" in data
    assert "private" in data
    assert "military" in data


@pytest.mark.asyncio
async def test_count_endpoint(client, admin_headers):
    """Count endpoint returns counts by type."""
    await client.post("/api/v1/universities/", json={
        "name": "Count Public", "location": "Kampala", "type": "public", "domains": [], "web_pages": []
    }, headers=admin_headers)
    await client.post("/api/v1/universities/", json={
        "name": "Count Private", "location": "Gulu", "type": "private", "domains": [], "web_pages": []
    }, headers=admin_headers)

    response = await client.get("/api/v1/universities/count")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data.get("public") == 1
    assert data.get("private") == 1
