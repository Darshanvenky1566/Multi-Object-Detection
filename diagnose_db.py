# -*- coding: utf-8 -*-
"""
NexVision MongoDB Connection Diagnostic Tool
Run: python diagnose_db.py
"""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME   = os.environ.get("DB_NAME", "nextvision")

print("=" * 60)
print("  NexVision MongoDB Connection Diagnostic")
print("=" * 60)

# 1. Check environment variables
print("\n[1] Environment Variables")
if MONGO_URI:
    # Mask password for security
    masked = MONGO_URI.split("@")
    if len(masked) == 2:
        creds = masked[0].split("://")
        if len(creds) == 2:
            user = creds[1].split(":")[0]
            masked_uri = f"{creds[0]}://{user}:****@{masked[1]}"
        else:
            masked_uri = MONGO_URI
    else:
        masked_uri = MONGO_URI
    print(f"  MONGO_URI: {masked_uri}")
else:
    print("  MONGO_URI: NOT SET!")
    print("  -> Add MONGO_URI to your .env file or environment variables.")
    sys.exit(1)

print(f"  DB_NAME:   {DB_NAME}")

# 2. Test connection
print("\n[2] Testing MongoDB Connection")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000, tlsAllowInvalidCertificates=True)
    info = client.server_info()
    print(f"  [OK] Connected to MongoDB server!")
    print(f"       Server version: {info.get('version', 'unknown')}")
    print(f"       Server name:    {info.get('name', 'unknown')}")
except ServerSelectionTimeoutError as e:
    print(f"  [FAIL] Cannot connect to MongoDB server (timeout)")
    print(f"         Error: {e}")
    print("\n  Possible causes:")
    print("  - IP address not whitelisted in MongoDB Atlas")
    print("  - Wrong credentials in MONGO_URI")
    print("  - Network/firewall blocking connection")
    print("  - MongoDB Atlas cluster is paused or down")
    print("\n  Fix: Go to MongoDB Atlas → Network Access → Add your IP to whitelist")
    sys.exit(1)
except PyMongoError as e:
    print(f"  [FAIL] MongoDB error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"  [FAIL] Unexpected error: {e}")
    sys.exit(1)

# 3. Check database and collections
print(f"\n[3] Checking Database '{DB_NAME}'")
db = client[DB_NAME]
collections = db.list_collection_names()
print(f"  Collections found: {collections}")

for col in ["users", "detections", "object_stats", "feedback"]:
    count = db[col].count_documents({})
    print(f"  {col:<20}: {count} document(s)")

# 4. Test insert + read
print("\n[4] Testing Insert + Read")
try:
    test_doc = {
        "user_id": "diagnostic_test",
        "original_filename": "test.jpg",
        "result_filename": "result_test.jpg",
        "objects_json": {"person": 1, "dog": 2},
        "total_objects": 3,
        "unique_objects": 2,
        "media_type": "image",
        "confidence": 0.45,
        "processing_time": 1.23,
        "created_at": datetime.now(timezone.utc)
    }
    result = db.detections.insert_one(test_doc)
    print(f"  [OK] Insert successful! ID: {result.inserted_id}")

    # Read it back
    doc = db.detections.find_one({"_id": result.inserted_id})
    print(f"  [OK] Read back: {doc['objects_json']}")

    # Clean up
    db.detections.delete_one({"_id": result.inserted_id})
    print(f"  [OK] Test document cleaned up.")
except Exception as e:
    print(f"  [FAIL] Insert/read test failed: {e}")
    print("\n  This could be caused by:")
    print("  - Schema validators rejecting the document (run create_db.py to check)")
    print("  - Collection doesn't exist or has wrong permissions")
    print("  - Data type mismatch in the document")

# 5. Check schema validators
print("\n[5] Checking Schema Validators")
for col in ["users", "detections", "object_stats", "feedback"]:
    try:
        info = db.command("listCollections", filter={"name": col})
        cols = list(info["cursor"]["idocuments"]) if "cursor" in info else []
        # Try alternative approach
        opts = db[col].options()
        if "validator" in opts:
            print(f"  {col}: HAS schema validator (may reject inserts)")
        else:
            print(f"  {col}: No schema validator")
    except Exception:
        print(f"  {col}: Unable to check (collection may not exist)")

print("\n" + "=" * 60)
print("  Diagnostic Complete!")
print("=" * 60)
client.close()
