from fastapi import FastAPI
from .database import Base, engine
from .routers import inventory
from .seed_data import seed_inventory_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Microservice", version="1.0")
app.include_router(inventory.router)

@app.on_event("startup")
def startup_event():
    seed_inventory_data()
