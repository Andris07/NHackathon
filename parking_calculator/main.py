from pathlib import Path

from datetime import datetime

HOUR = 3600
MINUTE = 60

def convert_to_total_seconds(START: str, END: str) -> int:
    START_date = datetime.strptime(START, "%Y-%m-%d %H:%M:%S")
    END_date = datetime.strptime(END, "%Y-%m-%d %H:%M:%S")
    seconds = int((END_date - START_date).total_seconds())

    return seconds

def convert_to_hours(seconds: int) -> int:
    return seconds // HOUR

def convert_to_minutes(seconds: int) -> int:
    return seconds // MINUTE

def remainder(seconds: int, base: int) -> int:
    return seconds % base

def breakdown(seconds: int):
    hours = convert_to_hours(seconds)
    remainder_after_hours = remainder(seconds, HOUR)

    minutes = convert_to_minutes(remainder_after_hours)
    remainder_after_minutes = remainder(remainder_after_hours, MINUTE)

    return hours, minutes, remainder_after_minutes

def parking_fee(START: str, END: str) -> int:
    seconds = convert_to_total_seconds(START, END)

    if seconds <= MINUTE * 30:
        return 0

    return seconds



def main():
    # data = Path("input.txt").read_text(encoding="utf-8")
    # print(data, end="")

    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")
    print(parking_fee("2026-03-30 07:00:00", "2026-03-30 07:30:00"))

if __name__ == "__main__":
    main()
