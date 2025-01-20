import os
import time
import requests
from subprocess import Popen, PIPE
import signal

def test_debug_mode():
    print("\nTesting Debug Mode Configuration...")
    
    # Test 1: Default (should be production mode)
    print("\n1. Testing default mode (should be production):")
    process = Popen(['python3', 'test.py'], stdout=PIPE, stderr=PIPE)
    time.sleep(2)  # Give the server time to start
    
    try:
        response = requests.get('http://localhost:5000/')
        print(f"Server responded with status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error making request: {str(e)}")
    
    process.terminate()
    out, err = process.communicate()
    print("Server output:", out.decode() if out else "None")
    print("Server errors:", err.decode() if err else "None")
    
    # Test 2: Explicit debug mode
    print("\n2. Testing explicit debug mode:")
    env = os.environ.copy()
    env['FLASK_DEBUG'] = 'true'
    process = Popen(['python3', 'test.py'], env=env, stdout=PIPE, stderr=PIPE)
    time.sleep(2)
    
    try:
        response = requests.get('http://localhost:5000/')
        print(f"Server responded with status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error making request: {str(e)}")
    
    process.terminate()
    out, err = process.communicate()
    print("Server output:", out.decode() if out else "None")
    print("Server errors:", err.decode() if err else "None")

def test_sql_injection():
    print("\nTesting SQL Injection Prevention...")
    
    process = Popen(['python3', 'test.py'], stdout=PIPE, stderr=PIPE)
    time.sleep(2)
    
    # Test normal query
    try:
        response = requests.get('http://localhost:5000/search?username=test')
        print("\nNormal query response:", response.text)
    except Exception as e:
        print(f"Error in normal query: {str(e)}")
    
    # Test injection attempt
    try:
        injection = "' OR '1'='1"
        response = requests.get(f'http://localhost:5000/search?username={injection}')
        print("\nInjection attempt response:", response.text)
    except Exception as e:
        print(f"Error in injection test: {str(e)}")
    
    process.terminate()
    process.wait()

if __name__ == "__main__":
    # Kill any existing Flask processes
    os.system("pkill -f 'python3 test.py'")
    time.sleep(1)
    
    # Install requests if not present
    os.system("pip install requests >/dev/null 2>&1")
    
    # Set up test database
    print("Setting up test database...")
    os.system("python3 setup_db.py")
    
    # Run tests
    test_debug_mode()
    test_sql_injection()
    
    print("\nVerification completed!")