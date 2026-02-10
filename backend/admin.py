from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from typing import List
import os
import uuid

# Router
router = APIRouter(prefix="/admin", tags=["Admin"])

# Database connection (gunakan config yang sama)
DATABASE_URL = "postgresql://playmate_db:PlaymateDB01%40@127.0.0.1:5432/playmate_db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# =========================
# SCHEMAS
# =========================
class SlotCreate(BaseModel):
    sport_id: int
    day: str
    time: str
    lapangan: str
    tingkat: str
    picture: str = None

# =========================
# ENDPOINTS
# =========================

# Dashboard Stats
@router.get("/stats")
def get_admin_stats():
    with engine.connect() as conn:
        # Total users
        total_users = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
        
        # Total sports
        total_sports = conn.execute(text("SELECT COUNT(*) FROM sports")).scalar()
        
        # Total slots
        total_slots = conn.execute(text("SELECT COUNT(*) FROM slots")).scalar()
        
        # Total revenue (CONFIRMED bookings)
        total_revenue = conn.execute(text("""
            SELECT COALESCE(SUM(sp.price), 0)
            FROM bookings b
            JOIN slots s ON s.id = b.slot_id
            JOIN sports sp ON sp.id = s.sport_id
            WHERE b.status = 'CONFIRMED'
        """)).scalar()
        
        # Bookings by status
        bookings_by_status = conn.execute(text("""
            SELECT status, COUNT(*) as count
            FROM bookings
            GROUP BY status
        """)).fetchall()
        
        # Popular sports
        popular_sports = conn.execute(text("""
            SELECT 
                sp.name,
                COUNT(b.id) as booking_count,
                ROUND(COUNT(b.id) * 100.0 / NULLIF((SELECT COUNT(*) FROM bookings WHERE status = 'CONFIRMED'), 0), 0) as percentage
            FROM sports sp
            LEFT JOIN slots s ON s.sport_id = sp.id
            LEFT JOIN bookings b ON b.slot_id = s.id AND b.status = 'CONFIRMED'
            GROUP BY sp.id, sp.name
            ORDER BY booking_count DESC
            LIMIT 5
        """)).fetchall()
        
        # Recent bookings
        recent_bookings = conn.execute(text("""
            SELECT 
                b.id,
                b.booking_name,
                u.name as user_name,
                u.email as user_email,
                sp.name as sport_name,
                s.day,
                s.time,
                b.status,
                b.created_at
            FROM bookings b
            JOIN users u ON u.id = b.user_id
            JOIN slots s ON s.id = b.slot_id
            JOIN sports sp ON sp.id = s.sport_id
            ORDER BY b.created_at DESC
            LIMIT 5
        """)).fetchall()
        
        return {
            "total_users": total_users,
            "total_sports": total_sports,
            "total_slots": total_slots,
            "total_revenue": total_revenue,
            "bookings_by_status": [dict(r._mapping) for r in bookings_by_status],
            "popular_sports": [dict(r._mapping) for r in popular_sports],
            "recent_bookings": [dict(r._mapping) for r in recent_bookings]
        }

# Get All Users
@router.get("/users")
def get_all_users():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id, name, email, provider, role, created_at
            FROM users
            ORDER BY created_at DESC
        """)).fetchall()
        
        return [dict(r._mapping) for r in rows]

# Delete User
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    with engine.begin() as conn:
        # Check if user exists
        user = conn.execute(
            text("SELECT id FROM users WHERE id = :id"),
            {"id": user_id}
        ).fetchone()
        
        if not user:
            raise HTTPException(404, "User tidak ditemukan")
        
        # Delete user's bookings first
        conn.execute(
            text("DELETE FROM bookings WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        
        # Delete user
        conn.execute(
            text("DELETE FROM users WHERE id = :id"),
            {"id": user_id}
        )
        
    return {"message": "User berhasil dihapus"}

# Add Sport
@router.post("/sports")
def add_sport(data: dict):
    with engine.begin() as conn:
        sport_id = conn.execute(text("""
            INSERT INTO sports (name, price, capacity)
            VALUES (:name, :price, :capacity)
            RETURNING id
        """), {
            "name": data["name"],
            "price": data["price"],
            "capacity": data["capacity"]
        }).scalar()
        
    return {"id": sport_id, "message": "Olahraga berhasil ditambahkan"}

# Update Sport
@router.put("/sports/{sport_id}")
def update_sport(sport_id: int, data: dict):
    with engine.begin() as conn:
        result = conn.execute(text("""
            UPDATE sports
            SET name = :name, price = :price, capacity = :capacity
            WHERE id = :id
            RETURNING id
        """), {
            "id": sport_id,
            "name": data["name"],
            "price": data["price"],
            "capacity": data["capacity"]
        }).fetchone()
        
        if not result:
            raise HTTPException(404, "Olahraga tidak ditemukan")
        
    return {"message": "Olahraga berhasil diupdate"}

# Delete Sport
@router.delete("/sports/{sport_id}")
def delete_sport(sport_id: int):
    with engine.begin() as conn:
        # Delete all bookings for this sport's slots
        conn.execute(text("""
            DELETE FROM bookings
            WHERE slot_id IN (
                SELECT id FROM slots WHERE sport_id = :sport_id
            )
        """), {"sport_id": sport_id})
        
        # Delete all slots for this sport
        conn.execute(
            text("DELETE FROM slots WHERE sport_id = :sport_id"),
            {"sport_id": sport_id}
        )
        
        # Delete sport
        result = conn.execute(
            text("DELETE FROM sports WHERE id = :id RETURNING id"),
            {"id": sport_id}
        ).fetchone()
        
        if not result:
            raise HTTPException(404, "Olahraga tidak ditemukan")
        
    return {"message": "Olahraga berhasil dihapus"}

# Get All Slots (with details)
@router.get("/slots")
def get_all_slots():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT 
                s.id,
                s.day,
                s.time,
                s.lapangan,
                s.tingkat,
                s.picture,
                sp.name as sport_name,
                sp.capacity,
                COUNT(b.id) as booked_count
            FROM slots s
            JOIN sports sp ON sp.id = s.sport_id
            LEFT JOIN bookings b ON b.slot_id = s.id AND b.status = 'CONFIRMED'
            GROUP BY s.id, s.day, s.time, s.lapangan, s.tingkat, s.picture, sp.name, sp.capacity
            ORDER BY s.day, s.time
        """)).fetchall()
        
        return [dict(r._mapping) for r in rows]

# Add Slot
@router.post("/slots")
def add_slot(data: SlotCreate):
    with engine.begin() as conn:
        slot_id = conn.execute(text("""
            INSERT INTO slots (sport_id, day, time, lapangan, tingkat, picture)
            VALUES (:sport_id, :day, :time, :lapangan, :tingkat, :picture)
            RETURNING id
        """), {
            "sport_id": data.sport_id,
            "day": data.day,
            "time": data.time,
            "lapangan": data.lapangan,
            "tingkat": data.tingkat,
            "picture": data.picture
        }).scalar()
        
    return {"id": slot_id, "message": "Slot berhasil ditambahkan"}

# Update Slot
@router.put("/slots/{slot_id}")
def update_slot(slot_id: int, data: SlotCreate):
    with engine.begin() as conn:
        result = conn.execute(text("""
            UPDATE slots
            SET sport_id = :sport_id, day = :day, time = :time,
                lapangan = :lapangan, tingkat = :tingkat, picture = :picture
            WHERE id = :id
            RETURNING id
        """), {
            "id": slot_id,
            "sport_id": data.sport_id,
            "day": data.day,
            "time": data.time,
            "lapangan": data.lapangan,
            "tingkat": data.tingkat,
            "picture": data.picture
        }).fetchone()
        
        if not result:
            raise HTTPException(404, "Slot tidak ditemukan")
        
    return {"message": "Slot berhasil diupdate"}

# Delete Slot
@router.delete("/slots/{slot_id}")
def delete_slot(slot_id: int):
    with engine.begin() as conn:
        # Delete all bookings for this slot
        conn.execute(
            text("DELETE FROM bookings WHERE slot_id = :slot_id"),
            {"slot_id": slot_id}
        )
        
        # Delete slot
        result = conn.execute(
            text("DELETE FROM slots WHERE id = :id RETURNING id"),
            {"id": slot_id}
        ).fetchone()
        
        if not result:
            raise HTTPException(404, "Slot tidak ditemukan")
        
    return {"message": "Slot berhasil dihapus"}

# Get All Bookings (with details)
@router.get("/bookings")
def get_all_bookings():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT 
                b.id,
                b.order_id,
                b.booking_name,
                b.status,
                b.created_at,
                u.name as user_name,
                u.email as user_email,
                sp.name as sport_name,
                sp.price,
                s.day,
                s.time,
                s.lapangan
            FROM bookings b
            JOIN users u ON u.id = b.user_id
            JOIN slots s ON s.id = b.slot_id
            JOIN sports sp ON sp.id = s.sport_id
            ORDER BY b.created_at DESC
        """)).fetchall()
        
        return [dict(r._mapping) for r in rows]

# Cancel Booking (Admin)
@router.put("/bookings/{booking_id}/cancel")
def admin_cancel_booking(booking_id: int):
    with engine.begin() as conn:
        result = conn.execute(text("""
            UPDATE bookings
            SET status = 'CANCELLED'
            WHERE id = :id
            RETURNING id
        """), {"id": booking_id}).fetchone()
        
        if not result:
            raise HTTPException(404, "Booking tidak ditemukan")
        
    return {"message": "Booking berhasil dibatalkan"}

# Delete Booking
@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int):
    with engine.begin() as conn:
        result = conn.execute(
            text("DELETE FROM bookings WHERE id = :id RETURNING id"),
            {"id": booking_id}
        ).fetchone()
        
        if not result:
            raise HTTPException(404, "Booking tidak ditemukan")
        
    return {"message": "Booking berhasil dihapus"}

# Upload Lapangan Photo
@router.post("/upload-lapangan")
async def upload_lapangan_photo(file: UploadFile = File(...)):
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"data/lapangan/{unique_filename}"
    
    # Create directory if not exists
    os.makedirs("data/lapangan", exist_ok=True)
    
    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Return URL
    return {"url": f"/data/lapangan/{unique_filename}"}