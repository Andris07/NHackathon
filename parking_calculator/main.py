from pathlib import Path
from datetime import datetime

DAY = 86400
HOUR = 3600
MINUTE = 60

def convert_to_total_seconds(start: str, end: str) -> int:
    startSeconds = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    endSeconds = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    seconds = int((endSeconds - startSeconds).total_seconds())

    return seconds

def parking_fee(start: str, end: str) -> int:
    seconds = convert_to_total_seconds(start, end)

    if seconds < 0:
        return -1

    days = seconds // DAY
    rest = seconds % DAY

    fee = days * 10000
    freeParking = rest - 30 * MINUTE

    if freeParking <= 0:
        return fee
    if freeParking <= 3 * HOUR:
        fee += (freeParking + HOUR - 1) // HOUR * 300
    else:
        fee += 3 * 300
        fee += ((freeParking - 3 * HOUR) + HOUR - 1) // HOUR * 500
    
    return fee

def main():
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")
    
    with open("fees.txt", "w", encoding="utf-8") as f:
        f.write("RENDSZÁM\tDÍJ\n")
        
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
