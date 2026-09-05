import argparse
import csv
import json
from pathlib import Path
from statistics import mean


def load_students(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def calculate_result(student):
    marks = [
        float(student["python"]),
        float(student["dbms"]),
        float(student["java"]),
    ]

    average = mean(marks)

    if average >= 40:
        result = "PASS"
    else:
        result = "FAIL"

    return {
        "name": student["name"],
        "average": round(average, 2),
        "result": result,
    }


def generate_report(input_file, output_file):
    students = load_students(input_file)

    reports = [
        calculate_result(student)
        for student in students
    ]

    Path(output_file).write_text(
        json.dumps(reports, indent=2),
        encoding="utf-8",
    )

    return reports


def main():
    parser = argparse.ArgumentParser(
        description="Automated Student Report Generator"
    )

    parser.add_argument(
        "--input",
        default="students.csv",
        help="Input CSV file",
    )

    parser.add_argument(
        "--output",
        default="student_report.json",
        help="Output JSON report",
    )

    args = parser.parse_args()

    reports = generate_report(
        args.input,
        args.output,
    )

    print("Student report generated successfully.")
    print(f"Students processed: {len(reports)}")
    print(f"Report saved to: {args.output}")


if __name__ == "__main__":
    main()
