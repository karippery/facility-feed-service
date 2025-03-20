import json
import time
import gzip
from pathlib import Path
from celery import shared_task
from django.conf import settings
from feed_service.models import Facility

@shared_task
def generate_facility_feed():
    """Generate facility feed files and metadata file."""
    timestamp = int(time.time())
    output_dir = Path(settings.FEED_OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    # Fetch all facilities
    facilities = Facility.objects.all().values(
        "id", "name", "phone", "url", "latitude", "longitude",
        "country", "locality", "region", "postal_code", "street_address"
    )
    total_records = len(facilities)
    chunk_size = 100

    # Generate feed files
    feed_files = []
    for i in range(0, total_records, chunk_size):
        chunk = facilities[i:i + chunk_size]
        feed_data = {"data": [transform_record(record) for record in chunk]}
        filename = f"facility_feed_{timestamp + i // chunk_size}.json.gz"
        filepath = output_dir / filename

        with gzip.open(filepath, "wt", encoding="utf-8") as f:
            json.dump(feed_data, f)
        feed_files.append(filename)

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