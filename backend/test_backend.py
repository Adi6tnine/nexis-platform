"""
Test if backend is running and responding
"""
import requests
import json

print("=" * 60)
print("Testing NEXIS Backend")
print("=" * 60)

base_url = "http://localhost:8000"

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
try:
    response = requests.get(f"{base_url}/")
    if response.status_code == 200:
        print("   ✓ Backend is running!")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ✗ Unexpected status: {response.status_code}")
except Exception as e:
    print(f"   ✗ Backend not responding: {e}")
    print("\n   Please start the backend:")
    print("   cd backend")
    print("   venv\\Scripts\\activate.bat")
    print("   uvicorn app.main:app --reload")
    exit(1)

# Test 2: Health check
print("\n2. Testing health endpoint...")
try:
    response = requests.get(f"{base_url}/health")
    print(f"   ✓ Status: {response.json()['status']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: CORS check
print("\n3. Testing CORS configuration...")
try:
    response = requests.get(f"{base_url}/health/cors")
    data = response.json()
    print(f"   ✓ CORS Status: {data['status']}")
    print(f"   Allowed origins: {data['allowed_origins']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Try registration (will fail if user exists, but tests endpoint)
print("\n4. Testing registration endpoint...")
try:
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123!"
    }
    response = requests.post(
        f"{base_url}/api/v1/auth/register",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        print("   ✓ Registration endpoint working!")
        print(f"   User created: {response.json()['user_id']}")
    elif response.status_code == 400:
        print("   ✓ Registration endpoint working!")
        print(f"   Note: {response.json()['detail']}")
    else:
        print(f"   ✗ Unexpected status: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("✅ Backend Test Complete!")
print("=" * 60)
print("\nIf all tests passed, the backend is working correctly.")
print("The CORS issue might be in the frontend configuration.")
print("\nNext steps:")
print("1. Make sure backend is running: uvicorn app.main:app --reload")
print("2. Make sure frontend is running: npm run dev")
print("3. Try accessing: http://localhost:3000 or http://localhost:3001")

input("\nPress Enter to exit...")
