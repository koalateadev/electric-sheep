import json


def _read_mapping(filename):
    with open(filename) as f:
        mapping = json.load(f)
    return mapping


def parse_cohorts(filename):
    mapping = _read_mapping(filename)
    return mapping


if __name__ == "__main__":
    mapping_file = "input/cohorts.json"
    print(parse_cohorts(mapping_file))