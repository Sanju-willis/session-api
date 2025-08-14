from uuid import uuid4
import hashlib

from src.core.db import SessionLocal
from src.models.conversation import Conversation
from src.types_.thread_types import Module, ThreadType

def generate_thread_id(user_id, company_id, module, thread_type):
    key = f"{user_id}:{company_id}:{module}:{thread_type}"
    return hashlib.md5(key.encode()).hexdigest()

def insert_dummy():
    db = SessionLocal()
    try:
        user_id = "2a3fc142-9e1e-43da-93c6-8292933195ad"
        company_id = "f1e806ce-b4f2-42dd-aec0-8cbc3544962d"
        module = Module.HOME.value
        thread_type = ThreadType.COMPANY.value

        convo = Conversation(
            id=uuid4(),
            user_id=user_id,
            company_id=company_id,
            module=module,
            thread_type=thread_type,
            context_id=None,
            thread_id=generate_thread_id(user_id, company_id, module, thread_type),
            stage="company_created",
            step="1"
        )
        db.add(convo)
        db.commit()
        print("✅ Inserted:", convo.id)
    except Exception as e:
        db.rollback()
        print("❌ Error inserting:", e)
    finally:
        db.close()

if __name__ == "__main__":
    insert_dummy()
