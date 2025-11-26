import pandas as pd
from typing import Dict, List
from dataclasses import dataclass
import re

from process.model.cohort_data import *


# Assuming the data structures are imported from your existing files
# from cohort_data import CohortData, WeekData, StudentData, QuestionAnswerData

def create_excel_from_cohort_data(cohort_data: CohortData, output_filename: str = "cohort_responses.xlsx"):
    """
    Converts CohortData structure to an Excel file with separate tabs for each week.

    Args:
        cohort_data: CohortData object containing all week data
        output_filename: Name of the output Excel file
    """

    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:

        for week_index, week_data in enumerate(cohort_data.weeks):
            # Create sheet name (Week 1, Week 2, etc.)
            sheet_name = f"Week {week_index + 1}"

            # Convert week data to DataFrame
            df = convert_week_to_dataframe(week_data)

            # Write to Excel sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Auto-adjust column widths
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass

                # Set column width with some padding
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 for readability
                worksheet.column_dimensions[column_letter].width = adjusted_width


def convert_week_to_dataframe(week_data: WeekData) -> pd.DataFrame:
    """
    Converts a single week's data to a pandas DataFrame.

    Args:
        week_data: WeekData object for a specific week

    Returns:
        DataFrame with students as rows and questions as columns
    """

    if not week_data.student_responses:
        return pd.DataFrame()

    # Collect all unique questions across all students
    all_questions = set()
    for student in week_data.student_responses:
        for qa in student.questions_answers:
            all_questions.add(qa.question)

    # Sort questions for consistent ordering
    sorted_questions = sorted(list(all_questions))

    # Create data for DataFrame
    data = []

    for student in week_data.student_responses:
        row = {"Student Name": student.name}

        # Create question-answer mapping for this student
        student_qa_map = {qa.question: qa.answer for qa in student.questions_answers}

        # Add answer for each question (empty string if student didn't answer)
        for question in sorted_questions:
            # Clean question text for column header
            clean_question = clean_question_text(question)
            row[clean_question] = student_qa_map.get(question, "")

        data.append(row)

    return pd.DataFrame(data)


def clean_question_text(question: str, max_length: int = 100) -> str:
    """
    Cleans question text to make it suitable for Excel column headers.

    Args:
        question: Original question text
        max_length: Maximum length for the cleaned question

    Returns:
        Cleaned question text
    """

    # Remove HTML entities and tags
    clean_text = re.sub(r'&[a-zA-Z]+;', '', question)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)

    # Remove extra whitespace
    clean_text = ' '.join(clean_text.split())

    # Truncate if too long and add ellipsis
    if len(clean_text) > max_length:
        clean_text = clean_text[:max_length - 3] + "..."

    return clean_text


def parse_csv_to_cohort_data(csv_file_path: str) -> CohortData:
    """
    Parses the CSV file and converts it to CohortData structure.
    This is a helper function to work with your existing CSV data.

    Args:
        csv_file_path: Path to the CSV file

    Returns:
        CohortData object
    """

    df = pd.read_csv(csv_file_path)

    # Group by section_name (which represents weeks)
    weeks_dict = {}

    for _, row in df.iterrows():
        week_name = row['section_name']
        student_name = row['student_name']
        question = row['question']
        answer = row['answer']

        # Initialize week if not exists
        if week_name not in weeks_dict:
            weeks_dict[week_name] = {}

        # Initialize student if not exists
        if student_name not in weeks_dict[week_name]:
            weeks_dict[week_name][student_name] = []

        # Add question-answer pair
        weeks_dict[week_name][student_name].append(
            QuestionAnswerData(question=question, answer=answer)
        )

    # Convert to CohortData structure
    weeks = []
    for week_name in sorted(weeks_dict.keys()):
        student_responses = []

        for student_name, qa_list in weeks_dict[week_name].items():
            student_data = StudentData(
                name=student_name,
                questions_answers=qa_list
            )
            student_responses.append(student_data)

        week_data = WeekData(student_responses=student_responses)
        weeks.append(week_data)

    return CohortData(weeks=weeks)


# Example usage function
def main():
    """
    Example of how to use the mapping functions.
    """

    # Option 1: If you already have CohortData object
    # create_excel_from_cohort_data(your_cohort_data, "output.xlsx")

    # Option 2: If you want to parse from CSV first
    csv_file_path = "responses.csv"
    cohort_data = parse_csv_to_cohort_data(csv_file_path)
    create_excel_from_cohort_data(cohort_data, "cohort_responses.xlsx")

    print("Excel file created successfully!")


if __name__ == "__main__":
    main()