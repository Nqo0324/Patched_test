import os
import time
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import json
import sys

def wait_for_server(port=5000, retries=5):
    for i in range(retries):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/')
            return True
        except urllib.error.URLError:
            print(f"Waiting for server (attempt {i+1}/{retries})...")
            time.sleep(1)
    return False

def run_test(debug_mode=False):
    print(f"\n{'='*20} Testing {'Debug' if debug_mode else 'Production'} Mode {'='*20}")
    
    # Set up environment
    env = os.environ.copy()
    env['FLASK_DEBUG'] = 'true' if debug_mode else 'false'
    
    # Start the Flask application
    flask_process = subprocess.Popen(['python3', 'test.py'], env=env, 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Starting Flask server...")
    if not wait_for_server():
        print("Failed to start server!")
        out, err = flask_process.communicate()
        print("Server stdout:", out.decode())
        print("Server stderr:", err.decode())
        flask_process.terminate()
        return False
    
    test_cases = [
        ('Normal search', f'http://127.0.0.1:5000/search?username=test'),
        ('SQL injection attempt', f'http://127.0.0.1:5000/search?username={urllib.parse.quote("' OR '1'='1")}'),
        ('Missing parameter', 'http://127.0.0.1:5000/search')
    ]
    
    for desc, url in test_cases:
        print(f"\nTest: {desc}")
        print(f"URL: {url}")
        try:
            response = urllib.request.urlopen(url)
            result = response.read().decode()
            print(f"Response: {result}")
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
            print(f"Response body: {e.read().decode()}")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Clean up
    flask_process.terminate()
    flask_process.wait()
    return True

if __name__ == '__main__':
    # First ensure database is ready
    print("Setting up database...")
    subprocess.run(['python3', 'setup_db.py'], check=True)
    
    # Run tests in both modes
    run_test(debug_mode=False)
    time.sleep(1)  # Wait between tests
    run_test(debug_mode=True)