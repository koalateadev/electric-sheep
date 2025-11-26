import json


def _read_mapping(filename):
    with open(filename) as f:
        mapping = json.load(f)
    return mapping


def parse_airtable_to_teachable_name(filename):
    return _read_mapping(filename)


if __name__ == "__main__":
    print(parse_airtable_to_teachable_name("input/airtable_name_to_teachable_name.json"))