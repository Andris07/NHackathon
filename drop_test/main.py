from pathlib import Path

def min_num_of_drops(N: int, H: int) -> int:
    if (H == 0):
        return 0
    elif (N == 1):
        return H

    K = 0
    drops = [0] * (N + 1)

    while drops[N] < H + 1:
        K += 1

        for n in range(N, 0, -1):
            drops[n] = drops[n] + drops[n - 1] + 1
    return K

def main():
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")

    for line in data.splitlines():
        N, H = line.split(",")
        print(min_num_of_drops(int(N), int(H)))

if __name__ == "__main__":
    main()
