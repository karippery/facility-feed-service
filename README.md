# Facility Feed Service
A Django application designed to generate JSON feed files from facility data stored in a PostgreSQL database, accompanied by a metadata file. The service processes data in chunks, and is fully containerized using Docker with Celery for asynchronous task execution and Redis as a message broker.

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

3. **Build and Start Docker Services**

    ``` docker-compose up --build ```

    **Starts:**
    - db: PostgreSQL (port 5433 by default)
    - redis: Redis (port 6379)
    - facility_feed_service: Django app (port 8000)
    - celery: Celery worker
     
 Access the Django server at http://localhost:8000 (or custom DJANGO_PORT).

4. **Apply Database Migrations**

    ```docker exec -it facility_feed_service python manage.py migrate ```

5. **Populate Fake Data** 

    ``` docker exec -it facility_feed_service python manage.py generate_feed ```
6. 
7. 

