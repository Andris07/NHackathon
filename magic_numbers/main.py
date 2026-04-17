from pathlib import Path

def convert(n: str) -> str:
    if "^" in n:
        base, exp = n.split("^")
        n = str(int(base) ** int(exp))
    return n

def next_magic_num(n: str) -> str:
    s = list(n)
    
    def mirror(arr):
        for i in range(len(arr) // 2):
            arr[-1 - i] = arr[i]
        return arr
    
    mirrored = "".join(mirror(s))
    if mirrored > n:
        return mirrored
    
    carry = 1
    i = (len(s) - 1) // 2
    while i >= 0 and carry:
        new = int(s[i]) + carry
        carry = new // 10
        s[i] = str(new % 10)
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
