from decouple import config
import os

print(f"Current working directory: {os.getcwd()}")
print(f"UNSPLASH_ACCESS_KEY from config: {config('UNSPLASH_ACCESS_KEY', default='NOT_FOUND')}")

# List files in current directory
print("Files in current directory:")
for f in os.listdir('.'):
    print(f)
