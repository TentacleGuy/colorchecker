# loader.py

import json

def load_json(file_path):
    """Lädt JSON-Daten aus einer Datei und gibt sie zurück."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def validate_data(data, schema):
    """Validiert die geladenen Daten gegen ein gegebenes Schema."""
    # Hier könnte eine Validierungslogik implementiert werden
    # z.B. mit jsonschema
    pass

def load_and_validate(file_path, schema):
    """Lädt JSON-Daten und validiert sie gegen ein Schema."""
    data = load_json(file_path)
    validate_data(data, schema)
    return data