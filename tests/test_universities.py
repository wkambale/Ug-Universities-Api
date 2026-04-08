import pytest


@pytest.fixture
def make_university():
    def _make(**kwargs):
        defaults = {
            "name": "Test University",
            "location": "Kampala",
            "type": "private",
            "domains": ["test.edu"],
            "web_pages": ["http://test.edu"],
        }
        return {**defaults, **kwargs}
    return _make


@pytest.mark.asyncio
async def test_create_university_no_auth(client, make_university):
    """Write endpoints should return 403 without a bearer token."""
    data = make_university()
    response = await client.post("/api/v1/universities/", json=data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_university(client, admin_headers, make_university):
    """Create a university with a valid admin token."""
    data = make_university()
    response = await client.post("/api/v1/universities/", json=data, headers=admin_headers)
    assert response.status_code == 201
    assert response.json()["data"]["name"] == "Test University"
    assert response.json()["data"]["is_active"] is True


@pytest.mark.asyncio
async def test_list_universities(client, admin_headers, make_university):
    """List endpoint should return paginated results."""
    await client.post("/api/v1/universities/", json=make_university(name="Makerere", type="public"), headers=admin_headers)
    await client.post("/api/v1/universities/", json=make_university(name="KIU", type="private"), headers=admin_headers)

    response = await client.get("/api/v1/universities/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["results"]) == 2
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_get_university(client, admin_headers, make_university):
    """Retrieve a single university by ID."""
    c_res = await client.post("/api/v1/universities/", json=make_university(), headers=admin_headers)
    u_id = c_res.json()["data"]["id"]

    response = await client.get(f"/api/v1/universities/{u_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == u_id


@pytest.mark.asyncio
async def test_get_university_not_found(client):
    """Should return 404 for non-existent university."""
    response = await client.get("/api/v1/universities/99999")
    assert response.status_code == 404
    assert response.json()["status"] == "error"


@pytest.mark.asyncio
async def test_update_university_put(client, admin_headers, make_university):
    """Full update (PUT) of an existing university."""
    c_res = await client.post("/api/v1/universities/", json=make_university(), headers=admin_headers)
    u_id = c_res.json()["data"]["id"]

    put_data = {
        "name": "Updated University",
        "location": "Entebbe",
        "type": "public",
    }
    put_res = await client.put(f"/api/v1/universities/{u_id}", json=put_data, headers=admin_headers)
    assert put_res.status_code == 200
    assert put_res.json()["data"]["name"] == "Updated University"
    assert put_res.json()["data"]["location"] == "Entebbe"


@pytest.mark.asyncio
async def test_update_university_patch(client, admin_headers, make_university):
    """Partial update (PATCH) of an existing university."""
    c_res = await client.post("/api/v1/universities/", json=make_university(), headers=admin_headers)
    u_id = c_res.json()["data"]["id"]

    patch_res = await client.patch(f"/api/v1/universities/{u_id}", json={"name": "New Name"}, headers=admin_headers)
    assert patch_res.status_code == 200
    assert patch_res.json()["data"]["name"] == "New Name"
    # Original fields should be preserved
    assert patch_res.json()["data"]["location"] == "Kampala"


@pytest.mark.asyncio
async def test_update_not_found(client, admin_headers):
    """Update a non-existent university should return 404."""
    res = await client.patch("/api/v1/universities/99999", json={"name": "Ghost"}, headers=admin_headers)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_university(client, admin_headers, make_university):
    """Soft-delete sets is_active=False; university no longer appears in default list."""
    c_res = await client.post("/api/v1/universities/", json=make_university(), headers=admin_headers)
    u_id = c_res.json()["data"]["id"]

    del_res = await client.delete(f"/api/v1/universities/{u_id}", headers=admin_headers)
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "success"

    # Verify soft delete — default list hides inactive
    get_res = await client.get("/api/v1/universities/")
    assert get_res.json()["count"] == 0

    # But querying with is_active=false should show it
    inactive_res = await client.get("/api/v1/universities/?is_active=false")
    assert inactive_res.json()["count"] == 1


@pytest.mark.asyncio
async def test_delete_not_found(client, admin_headers):
    """Delete a non-existent university should return 404."""
    res = await client.delete("/api/v1/universities/99999", headers=admin_headers)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_without_auth(client, admin_headers, make_university):
    """Delete without token should return 403."""
    c_res = await client.post("/api/v1/universities/", json=make_university(), headers=admin_headers)
    u_id = c_res.json()["data"]["id"]

    del_res = await client.delete(f"/api/v1/universities/{u_id}")
    assert del_res.status_code == 403
