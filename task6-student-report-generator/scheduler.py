import time
from datetime import datetime

from main import generate_report


def run_scheduled_report(
    input_file="students.csv",
    output_file="student_report.json",
    interval_seconds=60,
):
    print("Automated report scheduler started.")

    while True:
        try:
            generate_report(input_file, output_file)

            print(
                f"[{datetime.now().isoformat()}] "
                "Report generated successfully."
            )

        except (OSError, ValueError, KeyError) as error:
            print(f"Report generation failed: {error}")

        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_scheduled_report()
