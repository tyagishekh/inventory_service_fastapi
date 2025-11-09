from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from . import models
from sqlalchemy import func


TTL_MINUTES = 15

def get_inventory(db: Session, product_id: int):
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).all()

def reserve_stock(db: Session, product_id: int, warehouse: str, qty: int):
    inv = db.query(models.Inventory).filter_by(product_id=product_id, warehouse=warehouse).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")

    available = inv.on_hand - inv.reserved
    if available < qty:
        raise HTTPException(status_code=400,
                            detail=f"Insufficient stock. Reduce quantity to <= {available}.")

    inv.reserved += qty
    inv.reserved_at = datetime.utcnow()
    db.commit()
    db.refresh(inv)
    return inv

def release_stock(db: Session, product_id: int, warehouse: str, qty: int):
    inv = db.query(models.Inventory).filter_by(product_id=product_id, warehouse=warehouse).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")
    inv.reserved = max(inv.reserved - qty, 0)
    inv.reserved_at = None if inv.reserved == 0 else inv.reserved_at
    db.commit()
    db.refresh(inv)
    return inv

def ship_stock(db: Session, product_id: int, warehouse: str, qty: int):
    inv = db.query(models.Inventory).filter_by(product_id=product_id, warehouse=warehouse).first()
    if not inv or inv.reserved < qty:
        raise HTTPException(status_code=400, detail="Not enough reserved stock to ship")
    inv.reserved -= qty
    inv.on_hand -= qty
    inv.reserved_at = None if inv.reserved == 0 else inv.reserved_at
    db.commit()
    db.refresh(inv)
    return inv

def release_expired_reservations(db: Session):
    now = datetime.now(timezone.utc)
    cutoff_time = now - timedelta(minutes=TTL_MINUTES)

    expired = db.query(models.Inventory).filter(
        models.Inventory.reserved_at != None,
        models.Inventory.reserved_at < cutoff_time
    ).all()

    released_count = 0
    for inv in expired:
        inv.reserved = 0
        inv.reserved_at = None
        released_count += 1

    if released_count > 0:
        db.commit()
        print(f"✅ Released {released_count} expired reservations at {now.isoformat()}")

    return released_count
