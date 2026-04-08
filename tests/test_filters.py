import pytest


@pytest.fixture
def base_data():
    return {
        "domains": [],
        "web_pages": [],
    }


@pytest.mark.asyncio
async def test_filter_by_type(client, admin_headers, base_data):
    """Filter universities by type (public/private)."""
    await client.post("/api/v1/universities/", json={**base_data, "name": "Public Uni", "location": "Kampala", "type": "public"}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Private Uni", "location": "Entebbe", "type": "private"}, headers=admin_headers)

    res_public = await client.get("/api/v1/universities/?type=public")
    assert res_public.json()["count"] == 1
    assert res_public.json()["results"][0]["name"] == "Public Uni"

    res_private = await client.get("/api/v1/universities/?type=private")
    assert res_private.json()["count"] == 1
    assert res_private.json()["results"][0]["name"] == "Private Uni"


@pytest.mark.asyncio
async def test_filter_by_location(client, admin_headers, base_data):
    """Filter universities by location (case-insensitive partial match)."""
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni A", "location": "Kampala", "type": "public"}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni B", "location": "Gulu", "type": "private"}, headers=admin_headers)

    res_kampala = await client.get("/api/v1/universities/?location=Kampala")
    assert res_kampala.json()["count"] == 1
    assert res_kampala.json()["results"][0]["location"] == "Kampala"


@pytest.mark.asyncio
async def test_search(client, admin_headers, base_data):
    """Search across name, abbrev, and location fields."""
    await client.post("/api/v1/universities/", json={**base_data, "name": "Makerere", "location": "Kampala", "type": "public"}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Kyambogo", "location": "Kampala", "type": "public"}, headers=admin_headers)

    res_search = await client.get("/api/v1/universities/?search=makerere")
    assert res_search.json()["count"] == 1
    assert res_search.json()["results"][0]["name"] == "Makerere"


@pytest.mark.asyncio
async def test_search_by_location(client, admin_headers, base_data):
    """Search should also match location field."""
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni X", "location": "Gulu", "type": "public"}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Uni Y", "location": "Kampala", "type": "private"}, headers=admin_headers)

    res = await client.get("/api/v1/universities/?search=gulu")
    assert res.json()["count"] == 1
    assert res.json()["results"][0]["name"] == "Uni X"


@pytest.mark.asyncio
async def test_ordering_ascending(client, admin_headers, base_data):
    """Ordering by name ascending."""
    await client.post("/api/v1/universities/", json={**base_data, "name": "Zulu Uni", "location": "Kampala", "type": "public"}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Alpha Uni", "location": "Gulu", "type": "private"}, headers=admin_headers)

    res = await client.get("/api/v1/universities/?ordering=name")
    results = res.json()["results"]
    assert results[0]["name"] == "Alpha Uni"
    assert results[1]["name"] == "Zulu Uni"


@pytest.mark.asyncio
async def test_ordering_descending(client, admin_headers, base_data):
    """Ordering by name descending (prefix -)."""
    await client.post("/api/v1/universities/", json={**base_data, "name": "Zulu Uni", "location": "Kampala", "type": "public"}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "Alpha Uni", "location": "Gulu", "type": "private"}, headers=admin_headers)

    res = await client.get("/api/v1/universities/?ordering=-name")
    results = res.json()["results"]
    assert results[0]["name"] == "Zulu Uni"
    assert results[1]["name"] == "Alpha Uni"


@pytest.mark.asyncio
async def test_ordering_by_established(client, admin_headers, base_data):
    """Ordering by established year."""
    await client.post("/api/v1/universities/", json={**base_data, "name": "Old Uni", "location": "Kampala", "type": "public", "established": 1922}, headers=admin_headers)
    await client.post("/api/v1/universities/", json={**base_data, "name": "New Uni", "location": "Gulu", "type": "private", "established": 2015}, headers=admin_headers)

    res = await client.get("/api/v1/universities/?ordering=-established")
    results = res.json()["results"]
    assert results[0]["name"] == "New Uni"
    assert results[1]["name"] == "Old Uni"


@pytest.mark.asyncio
async def test_pagination(client, admin_headers, base_data):
    """Pagination controls page, page_size, total_pages, next, previous."""
    for i in range(25):
        await client.post("/api/v1/universities/", json={**base_data, "name": f"Uni {i:03d}", "location": "Kampala", "type": "public"}, headers=admin_headers)

    # Page 1
    res = await client.get("/api/v1/universities/?page=1&page_size=10")
    data = res.json()
    assert data["count"] == 25
    assert len(data["results"]) == 10
    assert data["total_pages"] == 3
    assert data["next"] is not None
    assert data["previous"] is None

    # Page 2
    res2 = await client.get("/api/v1/universities/?page=2&page_size=10")
    data2 = res2.json()
    assert len(data2["results"]) == 10
    assert data2["previous"] is not None
    assert data2["next"] is not None

    # Page 3 (last)
    res3 = await client.get("/api/v1/universities/?page=3&page_size=10")
    data3 = res3.json()
    assert len(data3["results"]) == 5
    assert data3["next"] is None
    assert data3["previous"] is not None


@pytest.mark.asyncio
async def test_filter_is_active(client, admin_headers, base_data):
    """is_active filter shows active (default) or inactive universities."""
    c_res = await client.post("/api/v1/universities/", json={**base_data, "name": "Active Uni", "location": "Kampala", "type": "public"}, headers=admin_headers)
    u_id = c_res.json()["data"]["id"]

    # Soft delete
    await client.delete(f"/api/v1/universities/{u_id}", headers=admin_headers)

    # Default should show 0
    res_default = await client.get("/api/v1/universities/")
    assert res_default.json()["count"] == 0

    # is_active=false shows the deleted one
    res_inactive = await client.get("/api/v1/universities/?is_active=false")
    assert res_inactive.json()["count"] == 1
