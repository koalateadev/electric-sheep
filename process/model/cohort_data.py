from dataclasses import dataclass


@dataclass
class QuestionAnswerData:
    question: str
    answer: str


@dataclass
class StudentData:
    name: str
    questions_answers: list[QuestionAnswerData]


@dataclass
class WeekData:
    student_responses: list[StudentData]


@dataclass
class CohortData:
    weeks: list[WeekData]