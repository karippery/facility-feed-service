# Facility Feed Service
A Django application designed to generate JSON feed files from facility data stored in a PostgreSQL database, accompanied by a metadata file. The service processes data in chunks, and is fully containerized using Docker with Celery for asynchronous task execution and Redis as a message broker.

## Overview
- **Purpose**: Generate and upload JSON feeds of facility data in gzip format to AWS S3.
- **Tech Stack**: Django, PostgreSQL, Celery, Redis, Python (asyncio), AWS S3.
- **Key Features**: 
  - Processes data in chunks (100 records per file) for memory efficiency.
  - Uses `asyncpg` for database queries and `aioboto3` for async S3 uploads.
  - Compresses feed files with gzip.
  - Dockerized for consistent deployment.
  - CI/CD via GitHub Actions to AWS ECR.

## Setup Instructions

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)
- Python 3.10 (optional, for local development outside Docker)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/karippery/facility-feed-service.git
   cd facility-feed-service

2. **Create a .env File (Optional)**
    The application uses defaults if no .env is provided. To customize settings, create a .env file in the project root:
    **Note:** .env is ignored by .gitignore—do not commit it.

## Containerization Approach

The application is split into multiple Docker containers, each handling a specific component of the system, orchestrated via Docker Compose. The key services are:

- **PostgreSQL**: A container running `postgres:15-alpine` to store facility data.
- **Redis**: A container using `redis:7-alpine` as the message broker and result backend for Celery.
- **Django Application**: A container built from a custom Dockerfile, running the core Django service on port 8000.
- **Celery Worker**: A separate container for asynchronous task processing (e.g., feed generation and S3 uploads), built from the same Dockerfile as the Django app.

### Key Features
- **Dependency Isolation**: Each service runs in its own container with isolated dependencies, avoiding conflicts.
- **Health Checks**: Containers include health checks (e.g., `pg_isready` for PostgreSQL, `redis-cli ping` for Redis) to ensure readiness before dependent services start.
- **Environment Configuration**: Environment variables (e.g., database credentials, AWS keys) are passed via a `.env` file, keeping sensitive data out of the codebase.
- **Volume Persistence**: Data volumes (e.g., `postgre/data`, `redis_data`) persist database and Redis state across container restarts.
- **Networking**: All services communicate over a custom Docker network (`app_network`) for secure, internal connectivity.
     
 Access the Django server at http://localhost:8000 (or custom DJANGO_PORT).

## How to Generate Data
Generate Fake Data
Use the Django management command to create 10,000 fake facility records with Faker:

      ``` docker-compose exec facility_feed_service python manage.py generate_fake_facilities ``` 

This populates the PostgreSQL database with test data (e.g., names, addresses, coordinates).

## How to Upload JSON Gzip Files to AWS S3
Trigger Feed Generation
Queue the feed generation task via Celery:

    ```docker-compose exec facility_feed_service python manage.py generate_feed``` 

## Approach

1. Initiate the Process
   - Trigger: The workflow begins when a user runs the Django management command python manage.py generate_feed.
   - Action: This queues a Celery task (generate_facility_feed) to handle the feed generation and upload asynchronously, keeping the main application responsive.

2. Read Facility Data from PostgreSQL
   - Source: Facility data (e.g., name, phone, location) is stored in a PostgreSQL database in the Facility model.
   - Chunked Retrieval: The Celery task uses asyncpg to fetch data in chunks (default: 100 records at a time) via an asynchronous query:
   - SQL: SELECT ... FROM feed_service_facility LIMIT 100 OFFSET <offset>.
   - The offset increments with each chunk (0, 100, 200, etc.) until all records are processed.
     Asynchronous database calls prevent blocking, allowing the system to handle large datasets efficiently.

3. Transform Data into Structured JSON
   - Processing: For each chunk of 100 records:
   - The task loops through the retrieved rows and transforms each record into a structured JSON object using the transform_record function.
   - Output: Each chunk becomes a JSON object with a "data" key containing an array of these transformed records (e.g., {"data": [<record1>, <record2>, ...]}).
   - Why Structured?: The format ensures compatibility with downstream systems (e.g., Google Reserve), providing a consistent, machine-readable structure.

4. Compress the JSON Feed
   - Compression: The JSON data for each chunk is encoded to UTF-8 and compressed using gzip to reduce file size.
   - Naming: Each compressed file is named dynamically (e.g., facility_feed_<timestamp + chunk_index>.json.gz), ensuring uniqueness and traceability.
   - Why Gzip?: Compression minimizes storage and transfer costs on AWS S3 while maintaining data integrity.

5. Upload Feed Files to AWS S3
   - Async Upload: The compressed JSON data is uploaded directly to an AWS S3 bucket using aioboto3 in an asynchronous operation:
   - Target: s3://facility-feed-bucket-2025-interview/feeds/<filename>.
   - Headers: ContentType: application/json, ContentEncoding: gzip.
   - No Local Storage: Files are streamed to S3 without writing to disk, optimizing resource use.
   - Tracking: The task maintains a list of uploaded filenames (e.g., feed_files) for inclusion in the metadata

6. Generate and Upload Metadata
- **Creation**: Once all chunks are processed and uploaded:
  - A metadata JSON object is created:

    ```json
    {
      "generation_timestamp": <timestamp>,
      "name": "reservewithgoogle.entity",
      "data_file": ["facility_feed_123456_0.json.gz", "facility_feed_123456_1.json.gz", ...]
    }

    ```
  - Upload: This metadata file is uploaded to S3 (uncompressed) at s3://facility-feed-bucket-2025-interview/feeds/metadata.json using the same async S3 client.
  - Why Metadata?: Provides context about the feed generation (e.g., when it happened, which files were created) for downstream consumers.

7. Complete the Workflow
   - Result: The Celery task returns a status object (e.g., {"status": "success", "feed_files": [...], "metadata_file": "metadata.json"}).
   - Verification: Users can check the S3 bucket to confirm the presence of feed files and metadata.
  
## Workflow Summary
- Start: Queue the task with generate_feed.
- Fetch: Asynchronously read facility data from PostgreSQL in chunks of 100.
- Transform: Convert each chunk into structured JSON with a defined schema.
- Compress: Gzip the JSON data for each chunk.
- Upload: Asynchronously send compressed feed files to AWS S3.
- Metadata: Create and upload a metadata file summarizing the process.
- Finish: Return success status and file details.

## Facility Feed Service - CI/CD Pipeline

The Facility Feed Service uses a CI/CD pipeline implemented with GitHub Actions to automate linting, testing, building, and deployment of the Dockerized application to AWS Elastic Container Registry (ECR). This ensures code quality, reliability, and seamless deployment to production.

### Pipeline Overview

The pipeline is triggered on code pushes, pull requests, or manual dispatch, running two main jobs: **linting/testing** and **building/pushing the Docker image**. It’s designed to catch issues early, validate functionality, and deploy only on the `main` branch.

#### Triggers
- **Push**: Runs on any branch, excluding changes only to Markdown files (`*.md`).
- **Pull Request**: Validates code against any branch.
- **Manual**: Allows triggering via the GitHub Actions UI (`workflow_dispatch`).

#### Jobs
1. **Lint and Test**
   - Runs on every push or pull request to ensure code quality and functionality.
   - Uses a PostgreSQL service for realistic testing.
2. **Build and Push**
   - Runs only on `main` branch pushes, after successful linting and testing.
   - Builds and pushes the Docker image to AWS ECR.
  
##  Sentry, JWT, and Swagger UI

The Facility Feed Service integrates **Sentry** for error tracking, **JWT** (JSON Web Tokens) for authentication, and **Swagger UI** (via `drf-spectacular`) for API documentation. These tools enhance monitoring, security, and usability of the application.

### Sentry

- **Purpose**: Monitors and tracks errors in the Django application and Celery tasks.
- **Usage**: Captures runtime exceptions and performance issues, sending them to a Sentry dashboard for analysis.
- **Setup**: Configured with a `SENTRY_DSN` environment variable in `.env` or `settings.py`.
- **Benefits**: Provides real-time error visibility, helping identify and resolve issues quickly.

### JWT (JSON Web Tokens)

- **Purpose**: Secures API endpoints with token-based authentication.
- **Usage**: Leverages `rest_framework_simplejwt` to issue and validate tokens for user access.
- **Setup**: Integrated into Django REST Framework via `INSTALLED_APPS` and authentication settings in `settings.py`.
- **Benefits**: Ensures only authorized users access protected routes, enhancing security.

### Swagger UI

- **Purpose**: Generates interactive API documentation.
- **Usage**: Uses `drf-spectacular` to auto-create a Swagger UI interface from the API schema.
- **Setup**: Added to `INSTALLED_APPS` in `settings.py`, with endpoints exposed via Django URLs.
- **Benefits**: Offers a user-friendly way to explore and test API endpoints, improving developer experience.

### Why These Tools?
- **Sentry**: Keeps the app reliable by catching errors early.
- **JWT**: Protects sensitive operations with robust authentication.
- **Swagger UI**: Simplifies API usage with clear, interactive docs.