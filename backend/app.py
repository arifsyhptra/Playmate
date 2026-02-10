from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, text
from google.oauth2 import id_token
from google.auth.transport import requests
import midtransclient
from admin import router as admin_router
from passlib.context import CryptContext
import time
from fastapi.staticfiles import StaticFiles

# =========================
# CONFIG
# =========================
DATABASE_URL = "postgresql://playmate_db:PlaymateDB01%40@127.0.0.1:5432/playmate_db"
GOOGLE_CLIENT_ID = "google-cliend-id"
MIDTRANS_SERVER_KEY = "server_key"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# =========================
# PASSWORD HASHING (FIX)
# =========================
# =========================
# PASSWORD HASHING (ARGON2 - MODERN & AMAN)
# =========================
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)# =========================
# FASTAPI APP
# =========================
app = FastAPI()
app.include_router(admin_router)

@app.get("/")
def root():
    return {
        "status": "Playmate API running",
        "docs": "/docs"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="data"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")

# =========================
# MIDTRANS SETUP
# =========================
snap = midtransclient.Snap(
    is_production=True,
    server_key=MIDTRANS_SERVER_KEY
)

# =========================
# SCHEMAS
# =========================
class RegisterIn(BaseModel):
    name: str
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

class BookingCreate(BaseModel):
    slot_id: int
    names: List[str]

class ParticipantIn(BaseModel):
    name: str
    phone: str

class OrderCreate(BaseModel):
    slot_id: int
    participant: ParticipantIn

class CreateOrder(BaseModel):
    slot_id: int
    participants: List[ParticipantIn]
    amount: int

class GoogleLoginIn(BaseModel):
    credential: str

class CreateTransactionRequest(BaseModel):
    slot_id: int
    name: str
    booking_name: str

# =========================
# AUTH ENDPOINTS
# =========================
@app.post("/auth/register")
def register(data: RegisterIn):
    hashed_password = hash_password(data.password)

    with engine.begin() as conn:
        user = conn.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": data.email}
        ).fetchone()

        if user:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")

        conn.execute(
            text("""
                INSERT INTO users (name, email, password, provider)
                VALUES (:name, :email, :password, 'local')
            """),
            {
                "name": data.name,
                "email": data.email,
                "password": hashed_password
            }
        )

    return {"message": "Register berhasil"}

@app.post("/auth/login")
def login(data: LoginIn):
    with engine.connect() as conn:
        user = conn.execute(
            text("""
                SELECT id, name, email, password, provider, role
                FROM users
                WHERE email = :email
            """),
            {"email": data.email}
        ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Password salah")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "provider": user.provider,
        "role": user.role
    }

@app.post("/auth/google-login")
def google_login(data: GoogleLoginIn):
    try:
        idinfo = id_token.verify_oauth2_token(
            data.credential,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo["email"]
        name = idinfo["name"]

        with engine.begin() as conn:
            user = conn.execute(
                text("SELECT id, name, email, role FROM users WHERE email = :email"),
                {"email": email}
            ).fetchone()

            if not user:
                user_id = conn.execute(
                    text("""
                        INSERT INTO users (name, email, provider)
                        VALUES (:name, :email, 'google')
                        RETURNING id
                    """),
                    {"name": name, "email": email}
                ).fetchone()[0]
                role = None
            else:
                user_id = user.id
                role = user.role

        return {
            "id": user_id,
            "name": name,
            "email": email,
            "provider": "google",
            "role": role
        }

    except Exception as e:
        print("GOOGLE LOGIN ERROR:", e)
        raise HTTPException(status_code=401, detail=str(e))

# =========================
# SPORTS & SLOTS
# =========================
@app.get("/sports")
def get_sports():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id, name, price, capacity
            FROM sports
            ORDER BY id
        """))
        return [dict(r._mapping) for r in rows]

@app.get("/sports/{sport_id}/slots")
def get_slots(sport_id: int):
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT
                    s.id,
                    s.day,
                    s.time,
                    s.lapangan,
                    s.tingkat,
                    s.picture,
                    sp.capacity,
                    COUNT(b.id) AS booked
                FROM slots s
                JOIN sports sp ON sp.id = s.sport_id
                LEFT JOIN bookings b
                  ON b.slot_id = s.id
                 AND b.status = 'CONFIRMED'
                WHERE s.sport_id = :sport_id
                GROUP BY
                    s.id,
                    s.day,
                    s.time,
                    s.lapangan,
                    s.tingkat,
                    s.picture,
                    sp.capacity
                ORDER BY s.day, s.time
            """),
            {"sport_id": sport_id}
        )
        return [dict(r._mapping) for r in rows]

@app.get("/slots/{slot_id}")
def get_slot(slot_id: int):
    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT
                s.id AS slot_id,
                sp.name AS sport_name,
                sp.price,
                sp.capacity
            FROM slots s
            JOIN sports sp ON sp.id = s.sport_id
            WHERE s.id = :slot_id
        """), {"slot_id": slot_id}).fetchone()

        if not row:
            raise HTTPException(404, "Slot tidak ditemukan")

        return dict(row._mapping)

@app.get("/slots/{slot_id}/participants")
def get_participants(slot_id: int):
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT 
                    id,
                    booking_name,
                    status
                FROM bookings
                WHERE slot_id = :slot_id
                AND status IN ('CONFIRMED', 'PENDING')
                ORDER BY id ASC
            """),
            {"slot_id": slot_id}
        ).fetchall()

        result = []
        for idx, r in enumerate(rows, start=1):
            result.append({
                "slot_number": idx,
                "booking_name": r.booking_name,
                "status": "paid" if r.status == "CONFIRMED" else "pending"
            })

        return result

# =========================
# BOOKINGS
# =========================
@app.post("/bookings")
def create_booking(data: BookingCreate):
    with engine.begin() as conn:
        booking_id = conn.execute(text("""
            INSERT INTO bookings (slot_id)
            VALUES (:slot_id)
            RETURNING id
        """), {"slot_id": data.slot_id}).scalar()

        for name in data.names:
            conn.execute(text("""
                INSERT INTO booking_participants (booking_id, name)
                VALUES (:booking_id, :name)
            """), {
                "booking_id": booking_id,
                "name": name
            })

    return {"ok": True}

@app.get("/bookings/by-email")
def get_bookings_by_email(email: str):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT
                    b.id,
                    b.order_id,
                    b.booking_name,
                    b.status,
                    b.created_at
                FROM bookings b
                JOIN users u ON u.id = b.user_id
                WHERE u.email = :email
                ORDER BY b.created_at DESC
            """),
            {"email": email}
        )
        rows = result.fetchall()

    return [dict(r._mapping) for r in rows]

@app.get("/booking-status")
def get_booking_status(order_id: str):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT status
                FROM bookings
                WHERE order_id = :order_id
            """),
            {"order_id": order_id}
        ).fetchone()

    if not row:
        raise HTTPException(404, "Booking tidak ditemukan")

    return {"status": row.status}

@app.post("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE bookings
                SET status = 'CANCELLED'
                WHERE id = :id
                AND status = 'PENDING'
                RETURNING id
            """),
            {"id": booking_id}
        )

        row = result.fetchone()

        if not row:
            raise HTTPException(
                status_code=400,
                detail="Booking tidak bisa dibatalkan"
            )

    return {"message": "Booking berhasil dibatalkan"}

# =========================
# TRANSACTIONS & MIDTRANS
# =========================
@app.post("/create-transaction")
def create_transaction(data: CreateTransactionRequest):
    try:
        order_id = f"ORDER-{data.slot_id}-{int(time.time())}"

        with engine.begin() as conn:
            slot = conn.execute(
                text("""
                    SELECT
                        s.id AS slot_id,
                        sp.name AS sport_name,
                        sp.price
                    FROM slots s
                    JOIN sports sp ON sp.id = s.sport_id
                    WHERE s.id = :slot_id
                """),
                {"slot_id": data.slot_id}
            ).fetchone()

            if not slot:
                raise HTTPException(404, "Slot tidak ditemukan")

            user = conn.execute(
                text("""
                    SELECT id, email, "NoHP"
                    FROM users
                    WHERE name = :name
                """),
                {"name": data.name}
            ).fetchone()

            if not user:
                raise HTTPException(404, "User tidak ditemukan")

            booking = conn.execute(
                text("""
                    INSERT INTO bookings (
                        slot_id,
                        booking_name,
                        user_id,
                        order_id,
                        status
                    )
                    VALUES (
                        :slot_id,
                        :booking_name,
                        :user_id,
                        :order_id,
                        'PENDING'
                    )
                    RETURNING id
                """),
                {
                    "slot_id": data.slot_id,
                    "booking_name": data.booking_name,
                    "user_id": user.id,
                    "order_id": order_id
                }
            ).fetchone()

        param = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": slot.price
            },
            "item_details": [
                {
                    "id": slot.slot_id,
                    "price": slot.price,
                    "quantity": 1,
                    "name": slot.sport_name
                }
            ],
            "customer_details": {
                "first_name": data.booking_name,
                "email": user.email,
                "phone": user.NoHP
            }
        }

        transaction = snap.create_transaction(param)

        return {
            "snap_token": transaction["token"],
            "order_id": order_id,
            "booking_id": booking.id
        }

    except Exception as e:
        print("MIDTRANS ERROR:", e)
        raise HTTPException(500, str(e))

@app.post("/midtrans/webhook")
async def midtrans_webhook(request: Request):
    payload = await request.json()

    order_id = payload.get("order_id")
    transaction_status = payload.get("transaction_status")

    if not order_id:
        return {"message": "no order_id"}

    if transaction_status == "settlement":
        status = "CONFIRMED"
    elif transaction_status == "pending":
        status = "PENDING"
    elif transaction_status in ["cancel", "expire", "deny"]:
        status = "FAILED"
    else:
        status = "UNKNOWN"

    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE bookings
                SET status = :status
                WHERE order_id = :order_id
            """),
            {
                "status": status,
                "order_id": order_id
            }
        )

    return {"message": "ok"}

# =========================
# ORDERS
# =========================
@app.post("/orders")
def create_order(data: OrderCreate):
    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT sp.price
            FROM slots s
            JOIN sports sp ON sp.id = s.sport_id
            WHERE s.id = :id
        """), {"id": data.slot_id}).fetchone()

        if not row:
            raise HTTPException(404, "Slot tidak ditemukan")

        amount = row.price

        order_id = conn.execute(text("""
            INSERT INTO orders (slot_id, amount, status)
            VALUES (:slot_id, :amount, 'PENDING')
            RETURNING id
        """), {
            "slot_id": data.slot_id,
            "amount": amount
        }).scalar()

        conn.execute(text("""
            INSERT INTO order_participants (order_id, name, phone)
            VALUES (:order_id, :name, :phone)
        """), {
            "order_id": order_id,
            "name": data.participant.name,
            "phone": data.participant.phone
        })

    snap_payload = {
        "transaction_details": {
            "order_id": f"ORDER-{order_id}",
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": data.participant.name,
            "phone": data.participant.phone
        },
        "enabled_payments": ["qris"]
    }

    snap_res = snap.create_transaction(snap_payload)

    return {
        "order_id": order_id,
        "snap_token": snap_res["token"]
    }