"""
Run once after first migration to seed PostgreSQL from JSON source.
Usage: python scripts/seed.py
"""
import asyncio
import json
import os
import sys

# Add the project root to the python path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal
from app.universities.models import University


async def seed():
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "uganda-universities-domains.json",
    )
    with open(json_path, "r") as f:
        records = json.load(f)

    async with AsyncSessionLocal() as db:
        for entry in records:
            # Support both old field names (uni_name, main_loc, lat, lon)
            # and new enriched field names (name, location, latitude, longitude)
            uni = University(
                name=entry.get("name") or entry.get("uni_name"),
                abbrev=entry.get("abbrev"),
                location=entry.get("location") or entry.get("main_loc"),
                type=entry.get("type", "private"),
                domains=entry.get("domains", []),
                web_pages=entry.get("web_pages", []),
                latitude=entry.get("latitude") or (float(entry["lat"]) if entry.get("lat") else None),
                longitude=entry.get("longitude") or (float(entry["lon"]) if entry.get("lon") else None),
                established=entry.get("established"),
                alpha_two_code=entry.get("alpha_two_code", "UG"),
                alpha_three_code=entry.get("alpha_three_code", "UGA"),
                country=entry.get("country", "Uganda"),
            )
            db.add(uni)
        await db.commit()

    print(f"Seeded {len(records)} universities successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
