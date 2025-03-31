import os
import sys

FEATURES_FILE_NAME='features.yml'

def find_paths_to_service_providers(directory: str) -> list[str]:
    provider_path = os.path.join(directory, 'provider.py')
    if os.path.isfile(provider_path):
        return [provider_path]
    paths = []
    for root, _, files in os.walk(directory):
        if 'provider.py' in files:
            paths.append(os.path.join(root, 'provider.py'))
    return paths


def map_features_files_status(services_path, changed_files) -> dict[str, bool]:
    missing_features_file_status = {}
    for file_path in changed_files:
        if file_path.startswith(services_path):
            service_folder_name = file_path.removeprefix(services_path).split('/')[1]
            service_path = os.path.join(services_path, service_folder_name)

            provider_files = find_paths_to_service_providers(service_path)
            for provider_file in provider_files:
                features_file = os.path.join(os.path.dirname(provider_file), FEATURES_FILE_NAME)
                missing_features_file_status[features_file] = os.path.exists(features_file)
    return missing_features_file_status

def main():
    # Detect changed features files
    comma_separated_changed_files = os.getenv('ALL_CHANGED_FILES')
    changed_files = comma_separated_changed_files.split(',')

    #Check features file exists in services folder
    services_path = os.getenv('SERVICES_PATH')
    features_file_status = map_features_files_status(services_path, changed_files)
    missing_files = [file_path for file_path, exists in features_file_status.items() if not exists]
    for file_path in missing_files:
            print(f"⚠️Feature file {file_path} is missing")
    if len(missing_files) != len(features_file_status):
        print(f"All feature files are missing")
        sys.exit(1)



if __name__ == "__main__":
    main()
