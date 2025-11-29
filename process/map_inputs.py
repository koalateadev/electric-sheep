import json
import os

from .parse_cohorts import parse_cohorts
from .parse_responses import parse_responses


def generate_output(parsed_input, parsed_mapping, parsed_student_ids):
    all_data = {}

    # Get unique weeks, users, and facilitators
    weeks = list(set(map(lambda response: response.section_name, parsed_input)))
    facilitators = list(parsed_mapping.keys())

    facilitators.append("Unknown")
    parsed_mapping["Unknown"] = []

    # Map students to facilitators for fast lookup
    student_to_facilitator = {}
    for lead, students in parsed_mapping.items():
        for student in students:
            student_to_facilitator[student] = lead

    # Hydrate base data structure
    for facilitator in facilitators:
        facilitator_data = {}
        all_data[facilitator] = facilitator_data
        for week in weeks:
            week_data = {}
            facilitator_data[week] = week_data
            for student in parsed_mapping[facilitator]:
                week_data[student] = {"responses": []}

    # Add all user submissions mapped off facilitator and session
    missing = set()
    for response in parsed_input:
        name = response.student_name
        week = response.section_name
        question = response.question
        answer = response.answer
        if name not in parsed_student_ids:
            print(f"Student {name} not found in mapping")
            missing.add(name)
            facilitator = "Unknown"
            airtable_name = name
        else:
            airtable_name = parsed_student_ids[name]
            if airtable_name not in student_to_facilitator:
                print(f"Student {name} not found in mapping")
                missing.add(name)
                facilitator = "Unknown"
            else:
                facilitator = student_to_facilitator[airtable_name]

        if airtable_name not in all_data[facilitator][week]:
            all_data[facilitator][week][airtable_name] = {"responses": []}

        all_data[facilitator][week][airtable_name]["responses"].append(
            {"question": question, "answer": answer},
        )

    return all_data, missing


if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    results_file_name = base_path + "/input/responses.csv"
    cohorts_file_name = base_path + "/input/cohorts.json"
    student_id_file_name = base_path + "/input/airtable_name_to_teachable_name.json"
    output_file_name = base_path + "/output/output.json"

    parsed_input = parse_responses(results_file_name)
    parsed_mapping = parse_cohorts(cohorts_file_name)
    parsed_student_ids = parse_cohorts(student_id_file_name)

    results, missing = generate_output(parsed_input, parsed_mapping, parsed_student_ids)
    print(missing)

    with open(output_file_name, 'w') as output_file:
        json.dump(results, output_file, indent=4)