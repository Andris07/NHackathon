from pathlib import Path

def min_height_when_it_breaks(tries: int, H: int) -> int:
    max_H = 0
    step = tries
    
    while step > 0 and max_H < H + 1:
        max_H += step
        step -= 1

    return max_H

def min_num_of_drops(N: int, H: int) -> int:
    if (H == 0):
        return 0
    elif (N == 1):
        return H

    K = 0

    # feltöltünk egy listát minden egyes leejtett eszköz "hibahatárával", vagyis azt az értéket, ahol még nem törik, és használható marad az eszköz
    drops = [0] * (N + 1)

    while drops[N] < H + 1:
        K += 1

        # frissítjük a listát a sikeres leejtések alapján
        for n in range(N, 0, -1):
            drops[n] = drops[n] + drops[n - 1] + 1

    return K

def main():
    # data = Path("input.txt").read_text(encoding="utf-8")
    # print(data, end="")
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")

    data = data.splitlines();
    for line in data:
        N, H = line.split(",")
        print(min_num_of_drops(int(N), int(H)))

if __name__ == "__main__":
    main()
