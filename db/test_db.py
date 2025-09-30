from database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    result = db.execute(text("SELECT NOW();"))  # ✅ wrap in text()
    print("✅ Connected to Aiven Postgres:", list(result))
except Exception as e:
    print("❌ Connection failed:", e)
finally:
    db.close()
