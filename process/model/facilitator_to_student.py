from dataclasses import dataclass

@dataclass
class FacilitatorToStudent:
    facilitator_name: str
    students: [str]