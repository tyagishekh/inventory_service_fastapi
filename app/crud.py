from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models

def get_inventory(db: Session, product_id: int):
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).all()

def reserve_stock(db: Session, product_id: int, warehouse: str, qty: int):
    inv = db.query(models.Inventory).filter_by(product_id=product_id, warehouse=warehouse).first()
    if not inv or inv.on_hand - inv.reserved < qty:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    inv.reserved += qty
    db.commit()
    db.refresh(inv)
    return inv

def release_stock(db: Session, product_id: int, warehouse: str, qty: int):
    inv = db.query(models.Inventory).filter_by(product_id=product_id, warehouse=warehouse).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")
    inv.reserved = max(inv.reserved - qty, 0)
    db.commit()
    db.refresh(inv)
    return inv

def ship_stock(db: Session, product_id: int, warehouse: str, qty: int):
    inv = db.query(models.Inventory).filter_by(product_id=product_id, warehouse=warehouse).first()
    if not inv or inv.reserved < qty:
        raise HTTPException(status_code=400, detail="Not enough reserved stock to ship")
    inv.reserved -= qty
    inv.on_hand -= qty
    db.commit()
    db.refresh(inv)
    return inv
