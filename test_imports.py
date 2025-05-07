import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    import langchain
    print(f"langchain version: {langchain.__version__}")
except ImportError as e:
    print(f"Error importing langchain: {e}")

try:
    import langchain_community
    print(f"langchain_community version: {langchain_community.__version__}")
except ImportError as e:
    print(f"Error importing langchain_community: {e}")

# Try to find the package location
try:
    import importlib.util
    print("\nChecking package locations:")
    for package in ['langchain', 'langchain_community']:
        spec = importlib.util.find_spec(package)
        if spec:
            print(f"{package} found at: {spec.origin}")
        else:
            print(f"{package} not found")
except Exception as e:
    print(f"Error checking package locations: {e}")
