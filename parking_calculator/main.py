from pathlib import Path
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

DAY = 86400
HOUR = 3600
MINUTE = 60

FREE_PERIOD = 30 * MINUTE
FIRST_PERIOD = 3 * HOUR

FIRST_RATE = 300
SECOND_RATE = 500
DAY_RATE = 10000

def convert_to_total_seconds(start: str, end: str) -> int:
    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    seconds = int((end_dt - start_dt).total_seconds())

    return seconds

def parking_fee(start: str, end: str) -> int:
    seconds = convert_to_total_seconds(start, end)

    if seconds < 0:
        return -1

    days = seconds // DAY
    rest = seconds % DAY

    fee = days * DAY_RATE
    billable_parking = rest - FREE_PERIOD

    if billable_parking <= 0:
        return fee
    if billable_parking <= FIRST_PERIOD:
        fee += (billable_parking + HOUR - 1) // HOUR * FIRST_RATE
        # fee += (billable_parking * FIRST_RATE + HOUR - 1) // HOUR
        # fee based on minutes for the extra points, the results are also integers
    else:
        fee += (FIRST_PERIOD // HOUR) * FIRST_RATE
        fee += ((billable_parking - FIRST_PERIOD) + HOUR - 1) // HOUR * SECOND_RATE
        # fee += ((billable_parking - FIRST_PERIOD) * SECOND_RATE + HOUR - 1) // HOUR
        # fee based on minutes for the extra points, the results are also integers
    
    return fee

def main():
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")
    
    with open(BASE_DIR / "fees.txt", "w", encoding="utf-8") as f:
        f.write("RENDSZAM\tDIJ\n")
        print("RENDSZAM\tDIJ")
        
        for line in data.splitlines()[2:]:
            parts = line.split()

            license_plate = parts[0]
            start = parts[1] + " " + parts[2]
            end = parts[3] + " " + parts[4]
            
            fee = parking_fee(start, end)

            if fee == -1:
                result = f"{license_plate}\t\tNem parkolt"
            else:
                result = f"{license_plate}\t\t{fee}"

            print(result)
            f.write(result + "\n")

if __name__ == "__main__":
    main()