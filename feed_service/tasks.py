import json
import os
import time
import gzip
import asyncio
from celery import shared_task
from django.conf import settings
import asyncpg
import aioboto3
from facility_feed_service.utils.logging_config import setup_logging

CHUNK_SIZE = int(os.getenv("FEED_CHUNK_SIZE", "100"))

# AWS S3 configuration
S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

logger = setup_logging()


async def fetch_facilities(offset: int = 0) -> list:
    """Fetch a chunk of facility records from the database."""
    
    try:
        conn = await asyncpg.connect(dsn=settings.DATABASE_URL)
        logger.info(f"Fetching facilities with offset: {offset}")
        rows = await conn.fetch(
            'SELECT id, name, phone, url, latitude, longitude, country, locality, region, postal_code, street_address '
            'FROM feed_service_facility LIMIT $1 OFFSET $2',
            CHUNK_SIZE, offset
        )
        return rows
    except Exception as e:
        logger.error(f"Error fetching facilities at offset {offset}: {e}", exc_info=True)
        return []
    finally:
        await conn.close()


async def upload_json_to_s3(data: dict, s3_key: str, is_gzipped: bool = False):
    """Upload JSON data to AWS S3 asynchronously."""
    try:
        async with aioboto3.Session().client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        ) as s3_client:
            json_data = json.dumps(data, ensure_ascii=False)
            if is_gzipped:
                json_data = gzip.compress(json_data.encode("utf-8"))
                extra_args = {"ContentType": "application/json", "ContentEncoding": "gzip"}
            else:
                extra_args = {"ContentType": "application/json"}
            logger.info(f"Uploading to S3 with key: {s3_key}")
            await s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_key,
                Body=json_data,
                **extra_args
            )
    except Exception as e:
        logger.error(f"Error uploading data to S3 with key {s3_key}: {e}", exc_info=True)


@shared_task
def generate_facility_feed():
    """Generate and upload facility feed files and metadata directly to AWS S3."""
    timestamp = int(time.time())
    feed_files = []
    offset = 0

    while True:
        facilities = asyncio.run(fetch_facilities(offset))
        if not facilities:
            logger.info(f"No facilities found at offset {offset}. Breaking the loop.")
            break

        # Transform records and prepare JSON data
        feed_data = {"data": [transform_record(record) for record in facilities]}
        filename = f"facility_feed_{timestamp + offset // CHUNK_SIZE}.json.gz"
        s3_key = f"feeds/{filename}"
        # Upload JSON data directly to S3
        asyncio.run(upload_json_to_s3(feed_data, s3_key, is_gzipped=True))
        feed_files.append(filename)

        offset += CHUNK_SIZE

    # Generate metadata file
    metadata = {
        "generation_timestamp": timestamp,
        "name": "reservewithgoogle.entity",
        "data_file": feed_files,
    }
    metadata_key = "feeds/metadata.json"
    asyncio.run(upload_json_to_s3(metadata, metadata_key, is_gzipped=False))
    logger.info(f"Generated feed files: {feed_files} and metadata file: {metadata_key}")
    return {"status": "success", "feed_files": feed_files, "metadata_file": "metadata.json"}


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
