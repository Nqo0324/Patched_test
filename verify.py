import subprocess
import time
import urllib.request
import urllib.error
import urllib.parse
import json
import os

def kill_flask():
    subprocess.run(['pkill', '-f', 'python3 test.py'], stderr=subprocess.DEVNULL)
    time.sleep(1)

def start_flask(debug=None):
    env = os.environ.copy()
    if debug is not None:
        env['FLASK_DEBUG'] = str(debug).lower()
    
    # Start Flask and redirect output
    with open('flask.log', 'w') as log:
        process = subprocess.Popen(['python3', 'test.py'], 
                                 env=env,
                                 stdout=log,
                                 stderr=subprocess.STDOUT)
    time.sleep(2)
    return process

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

print("Setting up test database...")
subprocess.run(['python3', 'setup_db.py'])

# Test 1: Debug Mode Default (should be False)
print("\n=== Test 1: Debug Mode Default ===")
kill_flask()
process = start_flask()
result = make_request('http://127.0.0.1:5000/')
print(f"Health check response: {result}")
with open('flask.log', 'r') as f:
    log_content = f.read()
print(f"Server log contains 'debugger' or 'debug mode': {'debugger' in log_content.lower() or 'debug mode' in log_content.lower()}")
kill_flask()

# Test 2: SQL Injection Prevention
print("\n=== Test 2: SQL Injection Prevention ===")
process = start_flask()
# Try SQL injection
injection_payload = "' OR '1'='1"
result = make_request(f'http://127.0.0.1:5000/search?username={urllib.parse.quote(injection_payload)}')
print(f"SQL Injection attempt response: {result}")
# Try normal query
result = make_request('http://127.0.0.1:5000/search?username=test')
print(f"Normal query response: {result}")
kill_flask()

# Test 3: Debug Mode Explicit Control
print("\n=== Test 3: Debug Mode Explicit Control ===")
# Try with debug True
process = start_flask(debug=True)
with open('flask.log', 'r') as f:
    log_content = f.read()
print("Debug=True log contains expected markers:", 'debug mode' in log_content.lower())
kill_flask()

# Try with debug False
process = start_flask(debug=False)
with open('flask.log', 'r') as f:
    log_content = f.read()
print("Debug=False log contains debug markers:", 'debug mode' in log_content.lower())
kill_flask()

print("\nAll tests completed!")