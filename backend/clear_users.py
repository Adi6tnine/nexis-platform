"""
Clear all users from database (for testing only)
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'nexis.db')

print("⚠️  WARNING: This will delete ALL users from the database!")
print(f"Database: {db_path}")
response = input("\nAre you sure? Type 'yes' to continue: ")

if response.lower() != 'yes':
    print("Cancelled.")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Count users before
    cursor.execute("SELECT COUNT(*) FROM users")
    count_before = cursor.fetchone()[0]
    print(f"\nUsers before: {count_before}")
    
    # Delete all users
    cursor.execute("DELETE FROM users")
    conn.commit()
    
    # Count users after
    cursor.execute("SELECT COUNT(*) FROM users")
    count_after = cursor.fetchone()[0]
    print(f"Users after: {count_after}")
    
    print(f"\n✅ Deleted {count_before} users")
    print("\nYou can now register a new account!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()

input("\nPress Enter to exit...")
