import os
from pathlib import Path

# =========================================================
# Project Name
# =========================================================

project_name = "playbook_product_review"

# =========================================================
# List of Files & Folders to Create
# =========================================================

list_of_files = [

    # Package files
    f"{project_name}/__init__.py",
    f"{project_name}/data_converter.py",
    f"{project_name}/data_ingestion.py",
    f"{project_name}/retriever_generation.py",

    # Frontend files
    "static/style.css",
    "templates/chat.html",

    # Main project files
    "setup.py",
    "app.py",
    "requirements.txt",
    ".env",
]

# =========================================================
# Create Files and Directories
# =========================================================

for filepath in list_of_files:

    filepath = Path(filepath)

    # Split directory and filename
    filedir, filename = os.path.split(filepath)

    # Create directories if they don't exist
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    # Create empty file if not exists
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:

        with open(filepath, "w") as f:
            pass

        print(f"✅ Created file: {filepath}")

    else:
        print(f"⚠️ File already exists: {filepath}")