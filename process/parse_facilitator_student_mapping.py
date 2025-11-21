import json


def read_mapping(mapping_file):
    """Read facilitator-student mapping from JSON file."""
    with open(mapping_file) as f:
        mapping = json.load(f)
    return mapping


def parse_mapping(mapping_file):
    """Parse facilitator to student mapping from JSON file."""
    try:
        mapping = read_mapping(mapping_file)
        return mapping
    except Exception as e:
        print(f"Error parsing mapping file: {e}")
        return []


if __name__ == "__main__":
    mapping_file = "input/facilitator_student_mapping.json"
    mapping = parse_mapping(mapping_file)
    print(mapping)