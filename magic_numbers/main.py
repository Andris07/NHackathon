from pathlib import Path

def next_magic_num(n: str) -> str:
    s = list(n)
    length = len(s)

    def mirror(arr):
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

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    print(data, end="")


if __name__ == "__main__":
    main()
