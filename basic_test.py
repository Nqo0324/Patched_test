#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import urllib.parse
import os

def test_server(debug_mode=False):
    # Set up environment
    env = os.environ.copy()
    env['FLASK_DEBUG'] = str(debug_mode).lower()
    env['PYTHONUNBUFFERED'] = '1'
    
    print(f"\nTesting with debug_mode={debug_mode}")
    print("-" * 50)
    
    # Start server
    process = subprocess.Popen(
        ['python3', '-u', 'test.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)  # Wait for server to start
    
    try:
        # Test health check
        print("Testing health check endpoint...")
        response = urllib.request.urlopen('http://localhost:5050/')
        print(f"Health check response: {response.read().decode()}")
        
        # Test normal search
        print("\nTesting normal search...")
        url = 'http://localhost:5050/search?username=' + urllib.parse.quote('test')
        response = urllib.request.urlopen(url)
        print(f"Normal search response: {response.read().decode()}")
        
        # Test SQL injection attempt
        print("\nTesting SQL injection prevention...")
        url = 'http://localhost:5050/search?username=' + urllib.parse.quote("' OR '1'='1")
        response = urllib.request.urlopen(url)
        print(f"SQL injection attempt response: {response.read().decode()}")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
    
    # Get server output
    process.terminate()
    stdout, stderr = process.communicate()
    print("\nServer stdout:")
    print(stdout.decode())
    print("\nServer stderr:")
    print(stderr.decode())
    
    time.sleep(1)

if __name__ == '__main__':
    # Kill any existing processes
    subprocess.run(['pkill', '-f', 'python3 test.py'], 
                  stderr=subprocess.DEVNULL,
                  stdout=subprocess.DEVNULL)
    time.sleep(1)
    
    # Test production mode
    test_server(debug_mode=False)
    
    # Test debug mode
    test_server(debug_mode=True)