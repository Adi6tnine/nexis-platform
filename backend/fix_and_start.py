"""
Fix database and start server
This script will:
1. Check/update database schema
2. Verify dependencies
3. Start the server
"""
import sqlite3
import os
import sys
import subprocess

print("=" * 70)
print("NEXIS Backend Setup & Start")
print("=" * 70)

# Check if we're in virtual environment
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("\n⚠️  WARNING: Virtual environment not activated!")
    print("\nPlease activate it first:")
    print("  venv\\Scripts\\activate.bat")
    input("\nPress Enter to exit...")
    exit(1)

print("\n✓ Virtual environment active")

# Path to database
db_path = os.path.join(os.path.dirname(__file__), 'nexis.db')

# Check if database exists
if not os.path.exists(db_path):
    print(f"\n⚠️  Database not found. It will be created on first run.")
else:
    print(f"\n✓ Database found: {db_path}")
    
    # Update database schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            print("✓ Users table exists")
            
            # Check columns
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Required authentication columns
            required = ['hashed_password', 'is_active', 'is_verified', 'profile_completed', 'last_login']
            missing = [col for col in required if col not in columns]
            
            if missing:
                print(f"\n⚠️  Adding {len(missing)} missing columns...")
                for col in missing:
                    if col == 'hashed_password':
                        cursor.execute(f"ALTER TABLE users ADD COLUMN {col} VARCHAR")
                    elif col == 'is_active':
                        cursor.execute(f"ALTER TABLE users ADD COLUMN {col} BOOLEAN DEFAULT 1")
                    elif col in ['is_verified', 'profile_completed']:
                        cursor.execute(f"ALTER TABLE users ADD COLUMN {col} BOOLEAN DEFAULT 0")
                    else:
                        cursor.execute(f"ALTER TABLE users ADD COLUMN {col} DATETIME")
                    print(f"   ✓ Added {col}")
                conn.commit()
                print("✓ Database schema updated")
            else:
                print("✓ All authentication columns present")
        
    except Exception as e:
        print(f"\n⚠️  Database check error: {e}")
    finally:
        conn.close()

# Check dependencies
print("\n📦 Checking dependencies...")
try:
    import fastapi
    import jose
    import passlib
    print("✓ All required packages installed")
except ImportError as e:
    print(f"\n❌ Missing dependency: {e}")
    print("\nInstalling dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

print("\n" + "=" * 70)
print("✅ Setup Complete! Starting server...")
print("=" * 70)
print("\nServer will start at: http://localhost:8000")
print("API docs available at: http://localhost:8000/docs")
print("\nPress Ctrl+C to stop the server")
print("=" * 70 + "\n")

# Start server
try:
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
except KeyboardInterrupt:
    print("\n\n👋 Server stopped")
