import urllib.request
import urllib.error
import os
import json
import time
import signal

def test_app(debug_mode=False):
    # Start the server with the appropriate debug mode
    if debug_mode:
        os.environ['FLASK_DEBUG'] = 'true'
    else:
        os.environ['FLASK_DEBUG'] = 'false'
    
    # Test cases
    test_cases = [
        {'username': 'test', 'description': 'Normal case'},
        {'username': "' OR '1'='1", 'description': 'SQL injection attempt'},
        {'username': None, 'description': 'Missing parameter'}
    ]
    
    print(f"\nTesting with debug_mode={debug_mode}")
    print("-" * 50)
    
    for test in test_cases:
        try:
            if test['username'] is None:
                url = "http://127.0.0.1:5000/search"
            else:
                url = f"http://127.0.0.1:5000/search?username={urllib.parse.quote(test['username'])}"
            
            print(f"\nTest: {test['description']}")
            print(f"URL: {url}")
            
            response = urllib.request.urlopen(url)
            result = response.read().decode('utf-8')
            print(f"Response: {result}")
            
        except urllib.error.HTTPError as e:
            print(f"Expected error for {test['description']}: {e.code} - {e.reason}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Test production mode
    test_app(debug_mode=False)
    
    # Test debug mode
    test_app(debug_mode=True)