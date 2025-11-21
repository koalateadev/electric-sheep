import json
from pprint import pprint

from parse_responses import parse_input, read_file
from itertools import groupby

from parse_facilitator_student_mapping import parse_mapping, read_mapping


def generate_output(input_file_name, mapping_file_name, output_file_name):
    input_lines = read_file(input_file_name)
    parsed_input = parse_input(input_lines)

    parsed_mapping = read_mapping(mapping_file_name)

    facilitator_results = {}
    for i in parsed_mapping:
        facilitator_results[i["facilitator"]] = {"results": []}

    weeks = list(set(map(lambda x: x["section_name"], parsed_input)))
    weeks.sort()
    # print(weeks)

    users = list(set(map(lambda x: x["student_name"], parsed_input)))
    users.sort()
    # print(users)

    all_users = []
    for facilitator in parsed_mapping:
        all_users.extend(facilitator["students"])
    all_users.sort()
    # print(all_users)

    all_data = []
    for week in weeks:
        all_data.append({"week": week, "users": []})
        for user in users:
            all_data[-1]["users"].append({"name": user, "answers": []})

    for i in parsed_input:
        name = i["student_name"]
        week = i["section_name"]
        answer = i["answer"]
        question = i["question"]
        all_data[weeks.index(week)]["users"][users.index(name)]["answers"].append({"question": question, "answer": answer})
    # pprint(all_data)

    with open(output_file_name, 'w') as output_file:
        json.dump(all_data, output_file, indent=4)


if __name__ == "__main__":
    input_file_name = "./process/input/responses.csv"
    mapping_file_name = "./process/input/facilitator_student_mapping.json"
    output_file_name = "./process/output/output.json"

    generate_output(input_file_name, mapping_file_name, output_file_name)