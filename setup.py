from setuptools import setup, find_packages
from typing import List


# =========================================================
# Function to Read requirements.txt
# =========================================================

def get_requirements() -> List[str]:
    """
    Reads the requirements.txt file
    and returns a list of dependencies.
    """

    requirement_list: List[str] = []

    try:
        with open("requirements.txt", "r") as file:

            # Read lines from requirements.txt
            requirements = file.readlines()

            # Remove newline characters
            requirement_list = [
                req.strip()
                for req in requirements
            ]

            # Remove empty lines
            requirement_list = [
                req for req in requirement_list
                if req != ""
            ]

            # Remove '-e .' if present
            if "-e ." in requirement_list:
                requirement_list.remove("-e .")

    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_list


# =========================================================
# Setup Configuration
# =========================================================

setup(
    name="playbook_product_review",
    version="0.1.0",
    packages=find_packages(),
    author="Justinfi.info",
    author_email="justinfi.info@gmail.com",
    install_requires=get_requirements(),
    description="A product review playbook using LangChain and LLMs."
)