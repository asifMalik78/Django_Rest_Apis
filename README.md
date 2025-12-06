# Storefront

## Docker Setup

### Prerequisites
- Docker and Docker Compose

### Running the Application

1. **Build and Run Containers**
   ```bash
   docker-compose up --build
   ```
   This will start:
   - Django Web App (port 8000)
   - MySQL Database (port 3307 mapped to 3306)
   - Redis
   - Celery Worker
   - Celery Beat

2. **Access the Site**
   Go to [http://localhost:8000](http://localhost:8000)

3. **Superuser**
   To create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Logs
To see logs:
```bash
docker-compose logs -f
```
