# Overview
Tools to help automate and improve the Electric Sheep fellowship process.

## Submission Segmentation
### Problem
Currently, Teachable only allows exporting an entire fellowship result as a single csv.
This is a problem for facilitators because they have to manually filter the results for their students each week.

### Goal
Create a simple script to take the Teachable submission output and a mapping between facilitators and students and output
an easily digestible output format broken out by facilitator and submission week.

### Info
URL: https://electricsheep.teachable.com/admin-app/courses/2778348/reports/open-ended-questions

Button: `Export CSV`

CSV Format: `student_name, section_name, lecture, question, answer, submitted_at`

### Potential Issues
- Student name missing or malformatted from the input list
- Buffer overflow if data input is too large
- CSV format changes
- Conflicts with student names
- Lack of stable sort by section name
- Selenium browser session times out

### Output Format
```json
[
  {
    "facilitator": "name 1",
    "results": [
      {
        "Week #": [
          {
            "Student Name": [
              "Answer 1",
              "Answer 2"
            ]
          }
        ]
      }
    ]
  }
]
```