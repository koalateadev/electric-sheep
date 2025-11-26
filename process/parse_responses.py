import csv
from datetime import datetime

from model.open_ended_response import OpenEndedResponse


def _read_file(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    return lines


def parse_responses(filename) -> list[OpenEndedResponse]:
    lines = _read_file(filename)

    parsed_lines = []
    csv_reader = csv.reader(lines)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        parsed_lines.append(
            OpenEndedResponse(
                student_name=row[0],
                section_name=row[1],
                lecture=row[2],
                question=row[3],
                answer=row[4],
                submitted_at=int(datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S').timestamp())
            )
        )
    return parsed_lines


if __name__ == '__main__':
    parsed_data = parse_responses('input/responses.csv')

    names = list(map(lambda x: x.section_name.lower(), parsed_data))
    filtered_names = list(set(names))
    filtered_names.sort()

    print(filtered_names)
