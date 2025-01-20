import urllib.request
import urllib.parse
import json
import os
import time
import subprocess
import sys

def make_request(url):
    try:
        response = urllib.request.urlopen(url)
        return {
            'status': response.getcode(),
            'data': json.loads(response.read().decode())
        }
    except urllib.error.HTTPError as e:
        return {
            'status': e.code,
            'data': json.loads(e.read().decode()) if e.headers.get_content_type() == 'application/json' else str(e)
        }
    except Exception as e:
        return {
            'status': -1,
            'error': str(e)
        }

def test_app(debug_mode):
    print(f"\n=== Testing with FLASK_DEBUG={debug_mode} ===")
    
    # Start Flask app
    env = os.environ.copy()
    env['FLASK_DEBUG'] = str(debug_mode).lower()
    process = subprocess.Popen(['python3', 'test.py'], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for app to start
    time.sleep(2)
    
    try:
        # Test 1: Health Check
        print("\n1. Testing health check endpoint...")
        result = make_request('http://localhost:5050/')
        print(f"Response: {result}")
        
        # Test 2: Normal Search
        print("\n2. Testing normal search...")
        result = make_request('http://localhost:5050/search?username=test')
        print(f"Response: {result}")
        
        # Test 3: SQL Injection Attempt
        print("\n3. Testing SQL injection prevention...")
        injection = "' OR '1'='1"
        encoded_injection = urllib.parse.quote(injection)
        result = make_request(f'http://localhost:5050/search?username={encoded_injection}')
        print(f"Response: {result}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Get server output
        process.terminate()
        stdout, stderr = process.communicate()
        print("\nServer stdout:")
        print(stdout.decode())
        print("\nServer stderr:")
        print(stderr.decode())
        time.sleep(1)

def main():
    # Kill any existing Flask processes
    subprocess.run(['pkill', '-f', 'python3 test.py'], 
                  stderr=subprocess.DEVNULL,
                  stdout=subprocess.DEVNULL)
    time.sleep(1)
    
    # Test both modes
    test_app(False)  # Production mode
    test_app(True)   # Debug mode

if __name__ == '__main__':
    main()