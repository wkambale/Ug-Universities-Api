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
    data = make_university()
    response = await client.post("/api/v1/universities/", json=data)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_university(client, make_university):
    data = make_university()
    headers = {"Authorization": "Bearer test-token"}
    response = await client.post("/api/v1/universities/", json=data, headers=headers)
    print("RESPONSE JSON:", response.json())
    assert response.status_code == 201
    assert response.json()["data"]["name"] == "Test University"

@pytest.mark.asyncio
async def test_list_universities(client, make_university):
    # Setup test data
    headers = {"Authorization": "Bearer test-token"}
    await client.post("/api/v1/universities/", json=make_university(name="Makerere", type="public"), headers=headers)
    await client.post("/api/v1/universities/", json=make_university(name="KIU", type="private"), headers=headers)

    response = await client.get("/api/v1/universities/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["results"]) == 2

@pytest.mark.asyncio
async def test_get_university(client, make_university):
    headers = {"Authorization": "Bearer test-token"}
    c_res = await client.post("/api/v1/universities/", json=make_university(), headers=headers)
    u_id = c_res.json()["data"]["id"]

    response = await client.get(f"/api/v1/universities/{u_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == u_id

@pytest.mark.asyncio
async def test_update_university(client, make_university):
    headers = {"Authorization": "Bearer test-token"}
    c_res = await client.post("/api/v1/universities/", json=make_university(), headers=headers)
    u_id = c_res.json()["data"]["id"]

    patch_res = await client.patch(f"/api/v1/universities/{u_id}", json={"name": "New Name"}, headers=headers)
    assert patch_res.status_code == 200
    assert patch_res.json()["data"]["name"] == "New Name"

@pytest.mark.asyncio
async def test_delete_university(client, make_university):
    headers = {"Authorization": "Bearer test-token"}
    c_res = await client.post("/api/v1/universities/", json=make_university(), headers=headers)
    u_id = c_res.json()["data"]["id"]

    del_res = await client.delete(f"/api/v1/universities/{u_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "success"

    # Verify soft delete
    get_res = await client.get("/api/v1/universities/")
    assert get_res.json()["count"] == 0
