import json


def extract_feature_metadata(file_path):
    """Reads the feature metadata JSON file and extracts key fields."""
    with open(file_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Extract required fields
    feature_info = {
        "feature_id": metadata.get("feature_id"),
        "feature_name": metadata.get("feature_name"),
        "description": metadata.get("description"),
        "data_type": metadata.get("data_type"),
        "units": metadata.get("units"),
        "source": metadata.get("source"),
        "creation_timestamp": metadata.get("creation_timestamp")
    }
    return feature_info


if __name__ == "__main__":
    # Path to the metadata file
    metadata_file = "metadata/feature_metadata.json"
    
    # Parse the metadata file and extract feature information
    feature_metadata = extract_feature_metadata(metadata_file)
    
    # Display the extracted feature metadata
    print("Extracted Feature Metadata:")
    for key, value in feature_metadata.items():
        print(f"{key}: {value}")
