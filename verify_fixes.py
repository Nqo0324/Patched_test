#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import urllib.request
import urllib.parse
import json

def wait_for_server(port, timeout=5):
    """Wait for server to start"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            urllib.request.urlopen(f'http://localhost:{port}/').read()
            return True
        except Exception:
            time.sleep(0.5)
    return False

def test_endpoint(url, method='GET', data=None):
    """Test an endpoint and return response"""
    try:
        if data:
            url += '?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        return {
            'status': response.status,
            'data': json.loads(response.read().decode())
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

def run_server(debug_mode=False):
    """Start the Flask server with specified debug mode"""
    env = os.environ.copy()
    env['FLASK_DEBUG'] = str(debug_mode).lower()
    return subprocess.Popen(
        ['python3', 'test.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )

def main():
    PORT = 5050
    
    print("Starting verification of fixes...")
    
    # Kill any existing Flask processes
    subprocess.run(['pkill', '-f', 'python3 test.py'], stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    # Test 1: Verify debug mode is off by default
    print("\n1. Testing Debug Mode Configuration:")
    server = run_server()
    if wait_for_server(PORT):
        response = test_endpoint(f'http://localhost:{PORT}/')
        print(f"Default mode response: {response}")
        output, error = server.communicate(timeout=1)
        print("Server output:", output.decode())
        if 'debugger' in output.decode().lower():
            print("WARNING: Debug mode appears to be enabled in default configuration")
    server.terminate()
    time.sleep(1)
    
    # Test 2: Verify SQL injection protection
    print("\n2. Testing SQL Injection Protection:")
    server = run_server()
    if wait_for_server(PORT):
        # Test normal query
        normal_response = test_endpoint(
            f'http://localhost:{PORT}/search',
            data={'username': 'test'}
        )
        print(f"Normal query response: {normal_response}")
        
        # Test SQL injection attempt
        injection_response = test_endpoint(
            f'http://localhost:{PORT}/search',
            data={'username': "' OR '1'='1"}
        )
        print(f"SQL injection attempt response: {injection_response}")
        
        if normal_response.get('data') == injection_response.get('data'):
            print("WARNING: SQL injection might still be possible")
    server.terminate()
    time.sleep(1)
    
    # Test 3: Verify debug mode can be enabled explicitly
    print("\n3. Testing Explicit Debug Mode:")
    server = run_server(debug_mode=True)
    if wait_for_server(PORT):
        response = test_endpoint(f'http://localhost:{PORT}/')
        print(f"Debug mode response: {response}")
        output, error = server.communicate(timeout=1)
        print("Server output:", output.decode())
        if 'debugger' not in output.decode().lower():
            print("WARNING: Debug mode not properly enabled when requested")
    server.terminate()

if __name__ == '__main__':
    main()