import pytest


@pytest.mark.asyncio
async def test_stats_empty(client):
    """Stats should return zeroed data when no universities exist."""
    response = await client.get("/api/v1/stats/")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 0
    assert data["active"] == 0
    assert data["by_type"] == {}
    assert data["by_location"] == {}


@pytest.mark.asyncio
async def test_stats_populated(client, admin_headers):
    """Stats should return correct totals and breakdowns."""
    base_data = {"domains": [], "web_pages": []}

    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni1", "location": "Kampala", "type": "public"}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni2", "location": "Entebbe", "type": "private"}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni3", "location": "Kampala", "type": "private"}, headers=admin_headers)

    response = await client.get("/api/v1/stats/")
    assert response.status_code == 200
    data = response.json()["data"]

    assert data["total"] == 3
    assert data["active"] == 3
    assert data["by_type"] == {"public": 1, "private": 2}
    assert data["by_location"] == {"Kampala": 2, "Entebbe": 1}


@pytest.mark.asyncio
async def test_stats_with_inactive(client, admin_headers):
    """Stats should correctly track total vs active after soft-deletes."""
    base_data = {"domains": [], "web_pages": []}

    c_res = await client.post("/api/v1/universities/", json={**base_data, "name": "Active Uni", "location": "Kampala", "type": "public"}, headers=admin_headers)
    c_res2 = await client.post("/api/v1/universities/", json={**base_data, "name": "Deleted Uni", "location": "Gulu", "type": "private"}, headers=admin_headers)
    u_id = c_res2.json()["data"]["id"]

    # Soft-delete one
    await client.delete(f"/api/v1/universities/{u_id}", headers=admin_headers)

    response = await client.get("/api/v1/stats/")
    data = response.json()["data"]

    assert data["total"] == 2  # total includes inactive
    assert data["active"] == 1  # only active ones
    assert data["by_type"] == {"public": 1}  # only active breakdown
