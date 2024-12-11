import os
import sys

# Ensure the parent directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from factory_management.factory import create_app

app = create_app()
print("App created successfully")


if __name__ == "__main__":
    app.run(debug=True)
