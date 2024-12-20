import os
import sys
from factory_management.factory import create_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create the Flask app using the factory function
app = create_app()
print("App created successfully")

if __name__ == "__main__":
    app.run(debug=True)

# run app by using "python -m factory_management.run" in terminal 
# then press Ctrl + c allow for the test command to be inputed while app is running 
# run "python -m unittest discover -s tests"
