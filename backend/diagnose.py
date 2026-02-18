"""
Diagnose backend issues
"""
import sys
import os

print("=" * 70)
print("NEXIS Backend Diagnostics")
print("=" * 70)

# Check Python version
print(f"\n1. Python Version: {sys.version}")

# Check if in virtual environment
in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
print(f"2. Virtual Environment: {'✓ Active' if in_venv else '✗ Not Active'}")

if not in_venv:
    print("\n⚠️  Please activate virtual environment:")
    print("   venv\\Scripts\\activate.bat")

# Check dependencies
print("\n3. Checking Dependencies:")
required = [
    'fastapi',
    'uvicorn',
    'sqlalchemy',
    'pydantic',
    'jose',
    'passlib',
    'slowapi'
]

missing = []
for pkg in required:
    try:
        __import__(pkg)
        print(f"   ✓ {pkg}")
    except ImportError:
        print(f"   ✗ {pkg} - MISSING")
        missing.append(pkg)

if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print("\nInstall with:")
    print("   pip install -r requirements.txt")

# Check database
db_path = os.path.join(os.path.dirname(__file__), 'nexis.db')
print(f"\n4. Database: {'✓ Exists' if os.path.exists(db_path) else '✗ Not Found'}")

# Check model files
model_path = os.path.join(os.path.dirname(__file__), 'models', 'credit_trust_model.pkl')
print(f"5. ML Model: {'✓ Exists' if os.path.exists(model_path) else '⚠️  Not Found (will be created on first run)'}")

# Try importing main app
print("\n6. Testing App Import:")
try:
    from app.main import app
    print("   ✓ App imports successfully")
    
    # Check CORS config
    print("\n7. CORS Configuration:")
    from app.core.config import settings
    print(f"   Allowed origins: {settings.BACKEND_CORS_ORIGINS}")
    
except Exception as e:
    print(f"   ✗ Error importing app: {e}")
    print("\n   This is the problem! Fix this error first.")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Diagnostics Complete")
print("=" * 70)

input("\nPress Enter to exit...")
