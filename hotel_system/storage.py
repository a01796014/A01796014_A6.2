"""
Storage utilities for JSON persistence.
"""

import json
import os


def load_data(filename):
    """Load JSON data safely from file."""
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as error:
        print(f"Error reading {filename}: {error}")
        return []


def save_data(filename, data):
    """Save JSON data safely to file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except IOError as error:
        print(f"Error writing {filename}: {error}")
