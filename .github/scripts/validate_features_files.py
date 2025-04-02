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
        print(f"Failed to parse JSON schema file: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Json schema file not found: {file_path}")
        sys.exit(1)

def validate_yaml_against_schema(yaml_data: str, json_schema: str, file_path: str) -> bool:
    try:
        validate(instance=yaml_data, schema=json_schema)
        print(f"Successful validation of file: {file_path}")
        return True
    except ValidationError as e:
        print(f"::notice file={file_path},title=Validation failed at path {' -> '.join(str(x) for x in e.path)}::{e.message}")
        return False

def main():
    # Detect changed features files
    comma_separated_changed_files = os.getenv('ALL_CHANGED_FILES')
    if not comma_separated_changed_files:
        print("Environment variable ALL_CHANGED_FILES is not set. Skipping validation.")
        sys.exit(1)

    changed_files = comma_separated_changed_files.split(',')
    changed_features_files = [path for path in changed_files if path.lower().endswith(FEATURES_FILE_NAME)]
    print(f'Changed features files: {",".join(changed_features_files)}')

    if len(changed_features_files) == 0:
        print('No feature file was changed. Skipping validation.')
        sys.exit(0)

    features_schema_path = os.getenv('FEATURES_JSON_SCHEMA', 'features_schema.json')
    features_schema = load_json_file(features_schema_path)
    print(f'Features schema file was loaded: {features_schema_path}')

    # validate schemas
    all_valid = True
    for file_path in changed_features_files:
        features_file = load_yaml_file(file_path)
        if not validate_yaml_against_schema(features_file, features_schema, file_path):
            all_valid = False
    sys.exit(0 if all_valid else 1)

if __name__ == "__main__":
    main()
