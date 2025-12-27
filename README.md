# ✈️ Airport API Service

REST API for an **airline booking system** built with **Django REST Framework (DRF)**.  
This service provides functionality for managing flights, tickets, orders, routes, and airports.  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Y-Havryliv/airport-api.git
cd airport-api
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
```bash
export DB_HOST=<your db hostname>
export DB_NAME=<your db name>
export DB_USER=<your db username>
export DB_PASSWORD=<your db user password>
export SECRET_KEY=<your secret key>
```

### 5. Run migrations and start server
```bash
python manage.py migrate
python manage.py runserver
```

---

## Features

- 🔑 **JWT authentication** – secure access with JSON Web Tokens  
- ⚙️ **Admin panel** – available at `/admin/`  
- 📑 **Interactive API documentation** – available at `/api/doc/swagger/`  
- 🎟️ **Tickets & Orders** – create and manage bookings  
- 🛫 **Flights management** – add and update flights  
- 🗺️ **Routes & Airports** – manage connections and locations  
- 🔍 **Filtering & Searching** – find flights by parameters  
- 🔒 **Permissions & Throttling** – access control and rate limiting  
- 🐳 **Docker support** – easy deployment with Docker  

---

## Run with Docker

```bash
docker-compose up --build
```



