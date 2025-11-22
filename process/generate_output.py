import json

from parse_facilitator_student_mapping import read_mapping
from parse_responses import parse_input, read_file


def generate_output(input_file_name, mapping_file_name, output_file_name):
    input_lines = read_file(input_file_name)
    parsed_input = parse_input(input_lines)

    parsed_mapping = read_mapping(mapping_file_name)

    weeks = list(set(map(lambda x: x["section_name"], parsed_input)))
    users = list(set(map(lambda x: x["student_name"], parsed_input)))
    facilitators = [facilitator["facilitator"] for facilitator in parsed_mapping]

    student_to_facilitator = {}
    for cohort in parsed_mapping:
        for student in cohort["students"]:
            student_to_facilitator[student] = cohort["facilitator"]

    all_data = {}
    for facilitator in facilitators:
        facilitator_data = {}
        all_data[facilitator] = facilitator_data
        for week in weeks:
            week_data = {}
            facilitator_data[week] = week_data
            for user in users:
                if student_to_facilitator[user.lower()] == facilitator:
                    week_data[user] = {"responses": []}

    for i in parsed_input:
        name = i["student_name"]
        week = i["section_name"]
        question = i["question"]
        answer = i["answer"]
        facilitator = student_to_facilitator[name.lower()]
        all_data[facilitator][week][name]["responses"].append(
            {"question": question, "answer": answer},
        )

    with open(output_file_name, 'w') as output_file:
        json.dump(all_data, output_file, indent=4)


if __name__ == "__main__":
    input_file_name = "./process/input/responses.csv"
    mapping_file_name = "./process/input/facilitator_student_mapping.json"
    output_file_name = "./process/output/output.json"

    generate_output(input_file_name, mapping_file_name, output_file_name)
