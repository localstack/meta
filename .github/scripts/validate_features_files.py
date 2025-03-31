import json
import os

import yaml
from jsonschema import validate, ValidationError
import sys

FEATURES_FILE_NAME='features.yml'

def load_yaml_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"YAML file not found: {file_path}")
        sys.exit(1)

def load_json_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON schema: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Schema file not found: {file_path}")
        sys.exit(1)

def validate_yaml_against_schema(yaml_data, json_schema):
    try:
        validate(instance=yaml_data, schema=json_schema)
        print("Validation successful, the YAML file matches JSON schema")
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        print(f"Failed at path: {' -> '.join(str(x) for x in e.path)}")
        return False

def main():
    # Detect changed features files
    comma_separated_changed_files = os.getenv('ALL_CHANGED_FILES')
    changed_files = comma_separated_changed_files.split(',')
    changed_features_files = [path for path in changed_files if path.lower().endswith(FEATURES_FILE_NAME)]
    print(f'Changed features files: {",".join(changed_features_files)}')

    features_schema_path = os.getenv('FEATURES_JSON_SCHEMA', 'features_schema.json')
    features_schema = load_json_file(features_schema_path)
    print(f'Features schema file was loaded: {features_schema_path}')

    # validate schemas
    for file_path in changed_features_files:
        features_file = load_yaml_file(file_path)
        validate_yaml_against_schema(features_file, features_schema)

if __name__ == "__main__":
    main()
