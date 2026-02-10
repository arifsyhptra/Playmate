"""
Script untuk membuat admin user
Usage: python create_admin.py
"""

from sqlalchemy import create_engine, text
import bcrypt
import sys

# Config
DATABASE_URL = "postgresql://playmate_db:PlaymateDB01%40@127.0.0.1:5432/playmate_db"

def create_admin_user():
    engine = create_engine(DATABASE_URL)
    
    print("=" * 50)
    print("CREATE ADMIN USER - PLAYMATE")
    print("=" * 50)
    
    # Input data admin
    name = input("\nNama Admin: ").strip()
    email = input("Email Admin: ").strip()
    password = input("Password: ").strip()
    
    if not name or not email or not password:
        print("❌ Semua field harus diisi!")
        return
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        with engine.begin() as conn:
            # Add role column if not exists
            conn.execute(text("""
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM information_schema.columns 
                        WHERE table_name = 'users' 
                        AND column_name = 'role'
                    ) THEN
                        ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';
                    END IF;
                END $$;
            """))
            
            # Check if email already exists
            existing = conn.execute(
                text("SELECT id, role FROM users WHERE email = :email"),
                {"email": email}
            ).fetchone()
            
            if existing:
                # Update existing user to admin
                conn.execute(
                    text("UPDATE users SET role = 'admin', password = :password WHERE email = :email"),
                    {"email": email, "password": hashed_password}
                )
                print(f"\n✅ User dengan email {email} berhasil diupdate menjadi admin!")
            else:
                # Create new admin user
                conn.execute(
                    text("""
                        INSERT INTO users (name, email, password, provider, role)
                        VALUES (:name, :email, :password, 'local', 'admin')
                    """),
                    {
                        "name": name,
                        "email": email,
                        "password": hashed_password
                    }
                )
                print(f"\n✅ Admin user berhasil dibuat!")
            
            print("\n" + "=" * 50)
            print("INFORMASI LOGIN:")
            print("=" * 50)
            print(f"Email    : {email}")
            print(f"Password : {password}")
            print("=" * 50)
            print("\n⚠️  Simpan informasi di atas dengan aman!")
            print("🔗 Login di: admin-login.html")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_admin_user()