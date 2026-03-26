import pytest

@pytest.mark.asyncio
async def test_export_json(client):
    headers = {"Authorization": "Bearer test-token"}
    await client.post("/api/v1/universities/", json={"name": "JSON Uni", "location": "Entebbe", "type": "public", "domains": [], "web_pages": []}, headers=headers)
    
    response = await client.get("/api/v1/universities/export/json")
    assert response.status_code == 200
    assert response.json()["data"][0]["name"] == "JSON Uni"

@pytest.mark.asyncio
async def test_export_csv(client):
    headers = {"Authorization": "Bearer test-token"}
    await client.post("/api/v1/universities/", json={"name": "CSV Uni", "location": "Jinja", "type": "private", "domains": ["csv.edu"], "web_pages": []}, headers=headers)
    
    response = await client.get("/api/v1/universities/export/csv")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/csv")
    csv_text = response.text
    assert "CSV Uni" in csv_text
    assert "csv.edu" in csv_text
