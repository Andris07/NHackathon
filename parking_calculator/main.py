from pathlib import Path

from datetime import datetime

def convert_to_total_seconds(START: datetime, END: datetime) -> int:
    START_date = datetime.strptime(START, "%Y-%m-%d %H:%M:%S")
    END_date = datetime.strptime(END, "%Y-%m-%d %H:%M:%S")
    seconds = (END_date - START_date).total_seconds()

    return seconds

def parking_fee(START: datetime, END: datetime) -> int:
    seconds = convert_to_total_seconds(START, END)
    
    return seconds

def main():
    # data = Path("input.txt").read_text(encoding="utf-8")
    # print(data, end="")

    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")
    print(parking_fee("2026-03-30 07:45:12", "2026-03-30 09:10:33"))

if __name__ == "__main__":
    main()
