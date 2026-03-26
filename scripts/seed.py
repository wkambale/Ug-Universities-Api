import asyncio
import json
import os
import sys

# Add the project root to the python path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal
from app.universities.models import University

async def seed():
    with open("uganda-universities-domains.json", "r") as f:
        records = json.load(f)

    async with AsyncSessionLocal() as db:
        for entry in records:
            # The source JSON currently has "uni_name", "main_loc", "lat", "lon" instead of
            # the fields expected in models.py (name, location, latitude, longitude)
            # and might lack "type" or "established". We handle mapping and defaults here.
            uni = University(
                name=entry.get("uni_name") or entry.get("name"),
                abbrev=entry.get("abbrev", ""),
                location=entry.get("main_loc") or entry.get("location"),
                type=entry.get("type", "private"),  # fallback to 'private'
                domains=entry.get("domains", []),
                web_pages=entry.get("web_pages", []),
                latitude=float(entry.get("lat")) if entry.get("lat") else entry.get("latitude"),
                longitude=float(entry.get("lon")) if entry.get("lon") else entry.get("longitude"),
                established=entry.get("established", None),
                alpha_two_code=entry.get("alpha_two_code", "UG"),
                alpha_three_code=entry.get("alpha_three_code", "UGA"),
                country=entry.get("country", "Uganda"),
            )
            db.add(uni)
        await db.commit()

    print(f"Seeded {len(records)} universities successfully.")

if __name__ == "__main__":
    asyncio.run(seed())
