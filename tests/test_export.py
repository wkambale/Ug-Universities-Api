import pytest
import json
import csv
import io


@pytest.mark.asyncio
async def test_export_json(client, admin_headers):
    """JSON export should return valid JSON with all university data."""
    await client.post("/api/v1/universities/", json={
        "name": "JSON Uni", "location": "Entebbe", "type": "public",
        "domains": ["json.edu"], "web_pages": ["http://json.edu"]
    }, headers=admin_headers)

    response = await client.get("/api/v1/universities/export/json")
    assert response.status_code == 200

    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "JSON Uni"

    # Verify it's valid parseable JSON
    parsed = json.loads(response.text)
    assert parsed["status"] == "success"


@pytest.mark.asyncio
async def test_export_json_multiple(client, admin_headers):
    """JSON export should include all universities."""
    for i in range(5):
        await client.post("/api/v1/universities/", json={
            "name": f"Uni {i}", "location": "Kampala", "type": "private",
            "domains": [], "web_pages": []
        }, headers=admin_headers)

    response = await client.get("/api/v1/universities/export/json")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5


@pytest.mark.asyncio
async def test_export_csv(client, admin_headers):
    """CSV export should return valid CSV with correct headers and data."""
    await client.post("/api/v1/universities/", json={
        "name": "CSV Uni", "location": "Jinja", "type": "private",
        "domains": ["csv.edu"], "web_pages": ["http://csv.edu"]
    }, headers=admin_headers)

    response = await client.get("/api/v1/universities/export/csv")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/csv")
    assert "attachment" in response.headers.get("Content-Disposition", "")

    csv_text = response.text
    assert "CSV Uni" in csv_text
    assert "csv.edu" in csv_text

    # Validate it's actually valid CSV
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    assert len(rows) == 1
    assert rows[0]["name"] == "CSV Uni"
    assert rows[0]["location"] == "Jinja"
