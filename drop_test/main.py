from pathlib import Path

def min_num_of_drops(N: int, H: int) -> int:
    if H == 0:
        return 0
    if N == 1:
        return H

    K = 0
    max_floors = [0] * (N + 1)

    while max_floors[N] < H:
        K += 1

        for n in range(N, 0, -1):
            max_floors[n] = max_floors[n] + max_floors[n - 1] + 1
    return K

def main():
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")

    for line in data.splitlines():
        N, H = line.split(",")
        print(min_num_of_drops(int(N), int(H)))

if __name__ == "__main__":
    main()
