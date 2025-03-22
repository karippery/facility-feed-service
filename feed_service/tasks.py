import json
import os
import time
import gzip
import asyncio
from pathlib import Path
from celery import shared_task
from django.conf import settings
import asyncpg

CHUNK_SIZE = int(os.getenv("FEED_CHUNK_SIZE", "100"))


async def fetch_facilities(offset: int = 0) -> list:
    """Fetch a chunk of facility records from the database."""
    conn = await asyncpg.connect(dsn=settings.DATABASE_URL)
    rows = await conn.fetch(
        'SELECT id, name, phone, url, latitude, longitude, country, locality, region, postal_code, street_address '
        'FROM feed_service_facility LIMIT $1 OFFSET $2',
        CHUNK_SIZE, offset
    )
    await conn.close()
    return rows


@shared_task
def generate_facility_feed():
    """Generate facility feed files and metadata file."""
    timestamp = int(time.time())
    output_dir = Path(settings.FEED_OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    feed_files = []
    offset = 0

    # Loop through chunks of facilities
    while True:
        # Run async fetch_facilities synchronously
        facilities = asyncio.run(fetch_facilities(offset))
        if not facilities:  # No more records to fetch
            break

        # Process the chunk
        feed_data = {"data": [transform_record(record) for record in facilities]}
        filename = f"facility_feed_{timestamp + offset // CHUNK_SIZE}.json.gz"
        filepath = output_dir / filename

        with gzip.open(filepath, "wt", encoding="utf-8") as f:
            json.dump(feed_data, f)
        feed_files.append(filename)

        offset += CHUNK_SIZE  # Move to the next chunk

    # Generate metadata file
    metadata = {
        "generation_timestamp": timestamp,
        "name": "reservewithgoogle.entity",
        "data_file": feed_files,
    }
    metadata_filepath = output_dir / "metadata.json"
    with open(metadata_filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    return {
        "status": "success",
        "feed_files": feed_files,
        "metadata_file": str(metadata_filepath),
    }


# Function to transform a facility record into the required JSON format
def transform_record(record):
    """Transform a facility record into the required JSON format."""
    return {
        "entity_id": f"dining-{record['id']}",
        "name": record["name"],
        "telephone": record["phone"],
        "url": record["url"],
        "location": {
            "latitude": float(record["latitude"]),
            "longitude": float(record["longitude"]),
            "address": {
                "country": record["country"],
                "locality": record["locality"],
                "region": record["region"],
                "postal_code": record["postal_code"],
                "street_address": record["street_address"],
            },
        },
    }