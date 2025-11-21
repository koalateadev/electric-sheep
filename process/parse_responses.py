import csv
from datetime import datetime


def read_file(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    return lines


def parse_input(lines):
    parsed_lines = []
    csv_reader = csv.reader(lines)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        parsed_lines.append(
            {
                'student_name': row[0],
                'section_name': row[1],
                'lecture': row[2],
                'question': row[3],
                'answer': row[4],
                'submitted_at': int(datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S').timestamp())
            },
        )
    return parsed_lines


if __name__ == '__main__':
    lines = read_file('input/responses.csv')
    parsed_data = parse_input(lines)

    names = list(map(lambda x: x["section_name"].lower(), parsed_data))
    filtered_names = list(set(names))
    filtered_names.sort()

    print(filtered_names)
