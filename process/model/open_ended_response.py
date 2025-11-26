from dataclasses import dataclass

@dataclass
class OpenEndedResponse:
    student_name: str
    section_name: str
    lecture: str
    question: str
    answer: str
    submitted_at: int