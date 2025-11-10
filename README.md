🏷️ Inventory Microservice

A FastAPI-based Inventory Management Microservice for e-commerce platforms.
It manages inventory across multiple warehouses, supports reservation, shipping, and release operations, and includes observability features such as metrics, structured logging, and dashboards.

🚀 Features
🧱 Core Inventory Operations

On-hand stock tracking

Reserve / Release / Ship inventory items atomically

Reservation TTL (15 min) with automatic reaper job

Manual reaper endpoint (/v1/inventory/reaper)

Validation for over-reservation (with helpful messages)

⚙️ Architecture

FastAPI – REST API framework

PostgreSQL – inventory database

SQLAlchemy ORM – database abstraction

APScheduler – background TTL reaper

Docker + Docker Compose – containerized services



🗂️ Directory Structure
inventory_service/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── database.py             # DB connection + Base model
│   ├── models.py               # SQLAlchemy model
│   ├── crud.py                 # Core DB operations
│   ├── routers/
│   │   └── inventory.py        # API endpoints
│   ├── seed_data.py            # Loads seed CSV into DB
│   ├── schemas.py              # Pydantic models
│   └── logs/                   # Structured JSON logs
│
├── seed/
│   └── inventory.csv           # Seed data
│
├── docker-compose.yml          # Multi-container setup
├── Dockerfile                  # FastAPI container
├── requirements.txt
└── README.md

🧰 Tech Stack
Component	Technology
Language	Python 3.13
Framework	FastAPI
Database	PostgreSQL
ORM	SQLAlchemy
Scheduler	APScheduler
Metrics	Prometheus
Dashboards	Grafana
Logging	Loguru
Containerization	Docker / Docker Compose
⚙️ Setup Instructions
🧩 1. Prerequisites

Docker & Docker Compose installed

Optional: pgAdmin 4 or DBeaver for DB access


🧱 2. Build and Run
docker-compose up --build


This will start:

FastAPI service → http://localhost:8000

PostgreSQL → on port 5432


🧠 3. Seed Data

The app automatically seeds initial inventory data from:

seed/inventory.csv


You can modify this file before running the containers.

🧪 4. Test API (via Swagger UI)

Go to:

👉 http://localhost:8000/docs

Available endpoints:

Method	Endpoint	Description
GET	/v1/inventory/onhand	Get on-hand stock for a product
POST	/v1/inventory/reserve	Reserve stock
POST	/v1/inventory/release	Release stock
POST	/v1/inventory/ship	Ship stock (reduce on_hand + reserved)
POST	/v1/inventory/reaper	Manually trigger expired reservation cleanup

🧠 Database Access

Connect via CMD, psql, pgAdmin, or DBeaver:

Key	Value
Host	localhost
Port	5432
Database	inventory_db
Username	user
Password	password

Example CMD commands:

docker ps

docker exec -it inventory_service_fastapi-inventory-db-1 psql -U user -d inventory_db

\dt

\d inventory

SELECT * FROM inventory

Example psql command:

psql -h localhost -U user -d inventory_db

🧹 Manual Reaper Testing

Manually set an old reservation:

UPDATE inventory SET reserved_at = now() - interval '20 minutes' WHERE product_id = 101;


Run:

curl -X POST http://localhost:8000/v1/inventory/reaper


Response:

{"released_reservations": 1}

🧩 Environment Variables
Variable	Default	Description
DATABASE_URL	postgresql://user:password@inventory-db:5432/inventory_db	DB connection URL
TTL_MINUTES	15	Reservation expiry window