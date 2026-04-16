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

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    print(data, end="")


if __name__ == "__main__":
    main()
