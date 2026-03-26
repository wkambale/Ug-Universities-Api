import pytest

@pytest.mark.asyncio
async def test_stats_empty(client):
    response = await client.get("/api/v1/stats/")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 0
    assert data["active"] == 0
    assert data["by_type"] == {}
    assert data["by_location"] == {}

@pytest.mark.asyncio
async def test_stats_populated(client):
    headers = {"Authorization": "Bearer test-token"}
    base_data = {
        "domains": [],
        "web_pages": [],
    }
    
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni1", "location": "Kampala", "type": "public"}, headers=headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni2", "location": "Entebbe", "type": "private"}, headers=headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni3", "location": "Kampala", "type": "private"}, headers=headers)

    response = await client.get("/api/v1/stats/")
    assert response.status_code == 200
    data = response.json()["data"]
    
    assert data["total"] == 3
    assert data["active"] == 3
    assert data["by_type"] == {"public": 1, "private": 2}
    assert data["by_location"] == {"Kampala": 2, "Entebbe": 1}
