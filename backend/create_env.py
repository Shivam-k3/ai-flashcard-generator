#!/usr/bin/env python3
"""
Script to create the .env file with Google API key
"""

import os

# The Google API key provided by the user
api_key = "AIzaSyCZPHxFgFdmY3YDJPAJDu81WYsWDS8fcFs"

# The name of the key for the .env file
key_name = "GOOGLE_API_KEY"

# Create the .env file content
env_content = f"{key_name}={api_key}\n"

# Define the path to the .env file in the same directory
env_path = os.path.join(os.path.dirname(__file__), '.env')

# Write to .env file, overwriting any existing content
with open(env_path, 'w') as f:
    f.write(env_content)

print("✅ .env file created/updated successfully!")
print(f"📁 Location: {env_path}")
print(f"🔑 {key_name} has been configured.")
print("\n🔄 Please restart your backend server for the changes to take effect.")
print("   (Stop with Ctrl+C, then run: python main.py)") 