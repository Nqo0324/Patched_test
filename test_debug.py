from test import app

# Get the debug status
debug_status = app.debug
print(f"Debug Mode Status: {debug_status}")

# Check if using development server configuration
if __name__ == '__main__' in app.import_name:
    print("WARNING: Using Flask development server configuration")