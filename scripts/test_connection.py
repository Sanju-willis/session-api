# scripts/test_connection.py
from sqlalchemy import text
from src.core.db import SessionLocal

def test_connection():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1")) 
        print("✅ DB connection successful")
    except Exception as e:
        print("❌ DB connection failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
# PYTHONPATH=. python scripts/test_connection.py
