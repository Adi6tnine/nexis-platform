"""
Manual database update script for authentication fields
Run this if alembic migration fails
"""
import sqlite3
import os

# Path to database
db_path = os.path.join(os.path.dirname(__file__), 'nexis.db')

print(f"Updating database: {db_path}")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    print(f"Current columns: {columns}")
    
    # Add authentication columns if they don't exist
    if 'hashed_password' not in columns:
        print("Adding hashed_password column...")
        cursor.execute("ALTER TABLE users ADD COLUMN hashed_password VARCHAR")
        print("✓ Added hashed_password")
    else:
        print("✓ hashed_password already exists")
    
    if 'is_active' not in columns:
        print("Adding is_active column...")
        cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1")
        print("✓ Added is_active")
    else:
        print("✓ is_active already exists")
    
    if 'is_verified' not in columns:
        print("Adding is_verified column...")
        cursor.execute("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0")
        print("✓ Added is_verified")
    else:
        print("✓ is_verified already exists")
    
    if 'profile_completed' not in columns:
        print("Adding profile_completed column...")
        cursor.execute("ALTER TABLE users ADD COLUMN profile_completed BOOLEAN DEFAULT 0")
        print("✓ Added profile_completed")
    else:
        print("✓ profile_completed already exists")
    
    if 'last_login' not in columns:
        print("Adding last_login column...")
        cursor.execute("ALTER TABLE users ADD COLUMN last_login DATETIME")
        print("✓ Added last_login")
    else:
        print("✓ last_login already exists")
    
    # Commit changes
    conn.commit()
    print("\n✅ Database updated successfully!")
    print("\nYou can now start the backend server:")
    print("  uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"\n❌ Error updating database: {e}")
    conn.rollback()
finally:
    conn.close()

print("\nPress Enter to exit...")
input()
