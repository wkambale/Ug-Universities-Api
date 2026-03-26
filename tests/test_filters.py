import pytest

@pytest.fixture
def base_data():
    return {
        "domains": [],
        "web_pages": [],
    }

@pytest.mark.asyncio
async def test_filter_by_type(client, base_data):
    headers = {"Authorization": "Bearer test-token"}
    await client.post("/api/v1/universities/", json={**base_data, "name": "Public Uni", "location": "Kampala", "type": "public"}, headers=headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Private Uni", "location": "Entebbe", "type": "private"}, headers=headers)

    res_public = await client.get("/api/v1/universities/?type=public")
    assert res_public.json()["count"] == 1
    assert res_public.json()["results"][0]["name"] == "Public Uni"

@pytest.mark.asyncio
async def test_filter_by_location(client, base_data):
    headers = {"Authorization": "Bearer test-token"}
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni A", "location": "Kampala", "type": "public"}, headers=headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni B", "location": "Gulu", "type": "private"}, headers=headers)

    res_kampala = await client.get("/api/v1/universities/?location=Kampala")
    assert res_kampala.json()["count"] == 1
    assert res_kampala.json()["results"][0]["location"] == "Kampala"

@pytest.mark.asyncio
async def test_search(client, base_data):
    headers = {"Authorization": "Bearer test-token"}
    await client.post("/api/v1/universities/", json={**base_data, "name": "Makerere", "location": "Kampala", "type": "public"}, headers=headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Kyambogo", "location": "Kampala", "type": "public"}, headers=headers)

    res_search = await client.get("/api/v1/universities/?search=makerere")
    assert res_search.json()["count"] == 1
    assert res_search.json()["results"][0]["name"] == "Makerere"

@pytest.mark.asyncio
async def test_pagination(client, base_data):
    headers = {"Authorization": "Bearer test-token"}
    for i in range(25):
        await client.post("/api/v1/universities/", json={**base_data, "name": f"Uni {i}", "location": "Kampala", "type": "public"}, headers=headers)
    
    res = await client.get("/api/v1/universities/?page=1&page_size=10")
    data = res.json()
    assert data["count"] == 25
    assert len(data["results"]) == 10
    assert data["total_pages"] == 3
    assert data["next"] is not None
    assert data["previous"] is None
