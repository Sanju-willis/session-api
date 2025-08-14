from src.core.db import SessionLocal
from src.models.user import User
from src.models.company import Company

def check_user_and_company():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        companies = db.query(Company).all()

        print("👤 Users:")
        for u in users:
            print(f" - {u.id} | {u.full_name} | {u.email}")

        print("\n🏢 Companies:")
        for c in companies:
            print(f" - {c.id} | {c.name}")

    except Exception as e:
        print("❌ Error fetching data:", e)
    finally:
        db.close()

if __name__ == "__main__":
    check_user_and_company()

# PYTHONPATH=. python scripts/check_user_company.py