#  Django Shopping Cart (Dockerized)

This is a Django-based shopping cart application, configured for local development using Docker and PostgreSQL.

---

##  Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/dockerized-my-cart-ecom.git
cd dockerized-my-cart-ecom

Create .env File
DEBUG=1
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypass

Build and Run Containers
docker-compose up --build

## Useful Commands
bash
Copy
Edit


# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

