import os
import time
import urllib.request
import urllib.error
import urllib.parse
import json
from subprocess import Popen, PIPE
import signal

def make_request(url):
    try:
        response = urllib.request.urlopen(url)
        return {
            'status': response.getcode(),
            'data': response.read().decode()
        }
    except urllib.error.HTTPError as e:
        return {
            'status': e.code,
            'error': e.read().decode()
        }
    except Exception as e:
        return {
            'status': -1,
            'error': str(e)
        }

def test_debug_mode():
    print("\nTesting Debug Mode Configuration...")
    
    # Test 1: Default (should be production mode)
    print("\n1. Testing default mode (should be production):")
    process = Popen(['python3', 'test.py'], stdout=PIPE, stderr=PIPE)
    time.sleep(2)
    
    result = make_request('http://localhost:5000/')
    print(f"Default mode response: {result}")
    
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
    
    result = make_request('http://localhost:5000/')
    print(f"Debug mode response: {result}")
    
    process.terminate()
    out, err = process.communicate()
    print("Server output:", out.decode() if out else "None")
    print("Server errors:", err.decode() if err else "None")

def test_sql_injection():
    print("\nTesting SQL Injection Prevention...")
    
    process = Popen(['python3', 'test.py'], stdout=PIPE, stderr=PIPE)
    time.sleep(2)
    
    # Test normal query
    result = make_request('http://localhost:5000/search?username=test')
    print("\nNormal query response:", result)
    
    # Test injection attempt
    injection = "' OR '1'='1"
    result = make_request(f'http://localhost:5000/search?username={urllib.parse.quote(injection)}')
    print("\nInjection attempt response:", result)
    
    process.terminate()
    process.wait()

if __name__ == "__main__":
    # Kill any existing Flask processes
    os.system("pkill -f 'python3 test.py'")
    time.sleep(1)
    
    # Set up test database
    print("Setting up test database...")
    os.system("python3 setup_db.py")
    
    # Run tests
    test_debug_mode()
    test_sql_injection()
    
    print("\nVerification completed!")