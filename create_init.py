import os

# Define the directories that need an __init__.py file
directories = [
    "App",
    "App/assets",
    "App/assets/Excel",
    "App/assets/json",
    "App/assets/QSS",
    "App/assets/QSS/mac",
    "App/assets/QSS/windows",
    "App/dialogs",
    "App/main_menu",
    "App/sr_counter",
    "App/utils",
]

# Create __init__.py files in the specified directories
for directory in directories:
    init_path = os.path.join(directory, "__init__.py")
    
    # Check if __init__.py already exists
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("# This file indicates that this directory should be treated as a package.\n")
        print(f"Created: {init_path}")
    else:
        print(f"Already exists: {init_path}")
