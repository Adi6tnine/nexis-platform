"""
Check and update database for authentication
Run this before starting the server
"""
import sqlite3
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Path to database
db_path = os.path.join(os.path.dirname(__file__), 'nexis.db')

print("=" * 60)
print("NEXIS Database Setup")
print("=" * 60)

if not os.path.exists(db_path):
    print(f"\n❌ Database not found at: {db_path}")
    print("\nPlease run the backend server first to create the database:")
    print("  uvicorn app.main:app --reload")
    input("\nPress Enter to exit...")
    exit(1)

print(f"\n📁 Database: {db_path}")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
        print("\n❌ Users table not found!")
        print("\nPlease run the backend server first to create tables:")
        print("  uvicorn app.main:app --reload")
        conn.close()
        input("\nPress Enter to exit...")
        exit(1)
    
    print("✓ Users table exists")
    
    # Check current columns
    cursor.execute("PRAGMA table_info(users)")
    columns = {col[1]: col[2] for col in cursor.fetchall()}
    
    print(f"\n📋 Current columns ({len(columns)}):")
    for col_name, col_type in columns.items():
        print(f"   - {col_name}: {col_type}")
    
    # Required authentication columns
    required_columns = {
        'hashed_password': 'VARCHAR',
        'is_active': 'BOOLEAN',
        'is_verified': 'BOOLEAN',
        'profile_completed': 'BOOLEAN',
        'last_login': 'DATETIME'
    }
    
    missing_columns = [col for col in required_columns if col not in columns]
    
    if not missing_columns:
        print("\n✅ All authentication columns exist!")
        print("\n🎉 Database is ready for authentication!")
    else:
        print(f"\n⚠️  Missing {len(missing_columns)} authentication columns")
        print("\nAdding missing columns...")
        
        for col_name in missing_columns:
            col_type = required_columns[col_name]
            print(f"   Adding {col_name}...")
            
            if col_name == 'is_active':
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type} DEFAULT 1")
            elif col_name in ['is_verified', 'profile_completed']:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type} DEFAULT 0")
            else:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            
            print(f"   ✓ Added {col_name}")
        
        conn.commit()
        print("\n✅ Database updated successfully!")
    
    # Check if there are any users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    print(f"\n👥 Current users: {user_count}")
    
    if user_count > 0:
        # Check if any users have passwords
        cursor.execute("SELECT COUNT(*) FROM users WHERE hashed_password IS NOT NULL")
        users_with_passwords = cursor.fetchone()[0]
        
        if users_with_passwords == 0:
            print("\n⚠️  Warning: Existing users don't have passwords!")
            print("   These users were created before authentication was added.")
            print("   They will need to register again with a password.")
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Start the backend: uvicorn app.main:app --reload")
    print("  2. Start the frontend: npm run dev")
    print("  3. Register a new account at http://localhost:3001")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()

print("\nPress Enter to exit...")
input()
