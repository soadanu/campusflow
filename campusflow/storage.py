"""JSON persistence."""

import json
import os

DEFAULT_PATH = os.path.join("data", "tickets.json")
REQUIRED_FIELDS = {
    "id", "title", "category", "urgency",
    "affected_users", "priority", "status", "assigned_to",
}


class StorageError(Exception):
    """The ticket file exists but cannot be trusted."""


def load_tickets(path=DEFAULT_PATH):
    """Missing file -> fresh start. Bad file -> StorageError (never silently erased)."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise StorageError(f"{path} is not valid JSON ({error}). Fix or move the file.") from error
    except OSError as error:
        raise StorageError(f"Could not read {path}: {error}") from error

    if not isinstance(data, list):
        raise StorageError(f"{path} must contain a list of tickets.")
    for item in data:
        if not isinstance(item, dict) or not REQUIRED_FIELDS.issubset(item):
            raise StorageError(f"{path} contains a ticket with missing fields.")
    return data


def save_tickets(tickets, path=DEFAULT_PATH):
    """Write to a temp file, then swap it in, so a crash cannot leave half a file."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    temp_path = path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2)
    os.replace(temp_path, path)
