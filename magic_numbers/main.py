from pathlib import Path

def convert(n: str) -> str:
    n = n.strip()
    if "^" in n:
        base, exp = n.split("^")
        n = str(int(base) ** int(exp))
    return n

def mirror(arr):
    for i in range(len(arr) // 2):
        arr[-1 - i] = arr[i]
    return arr

def next_magic_num(n: str) -> str:
    s = list(n)
    
    mirrored = "".join(mirror(s.copy()))
    if mirrored > n:
        return mirrored
    
    carry = 1
    i = (len(s) - 1) // 2

    while i >= 0 and carry:
        total = int(s[i]) + carry
        carry = total // 10
        s[i] = str(total % 10)
        i -= 1

    if carry:
        return "1" + "0" * (len(s) - 1) + "1"

    mirror(s)
    return "".join(s)

def main():
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")

    for n in data.splitlines():
        print(next_magic_num(convert(n)))

if __name__ == "__main__":
    main()
