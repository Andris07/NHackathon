from pathlib import Path

def convert(data: str) -> str:
    total = 0

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        # ha van ^, akkor hatvány
        if "^" in line:
            base, exp = line.split("^")
            total += int(base) ** int(exp)
        else:
            # sima szám
            digits = "".join(ch for ch in line if ch.isdigit())
            if digits:
                total += int(digits)

    return str(total)

def next_magic_num(n: str) -> str:
    s = list(n)
    length = len(s)

    def mirror(arr):
        arr = arr.copy()
        l = len(arr)
        for i in range(l // 2):
            arr[l - 1 - i] = arr[i]
        return arr
    
    mirrored = mirror(s.copy())
    if "".join(mirrored) > n:
        return "".join(mirrored)
    
    carry = 1
    mid = (length - 1) // 2

    i = mid
    while i >= 0 and carry:
        new = int(s[i]) + carry
        carry = new // 10
        s[i] = str(new % 10)
        i -= 1

    if carry:
        return "1" + "0" * (length - 1) + "1"

    return "".join(mirror(s))



def main():
    # data = Path("input.txt").read_text(encoding="utf-8")
    # print(data, end="")
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")

    numbers = data.splitlines()
    for n in numbers:
        print(next_magic_num(convert(n)))

if __name__ == "__main__":
    main()
