#!/usr/bin/env python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
print("Loading environment variables...")
load_dotenv(verbose=True)

# Check for API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print(f"API key found! Length: {len(api_key)}")
    print(f"First few characters: {api_key[:5]}...")
else:
    print("API key not found!")
    print("Please make sure your .env file contains: ANTHROPIC_API_KEY=your_key_here")
