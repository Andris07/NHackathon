from pathlib import Path

def min_height_when_it_breaks(tries: int, H: int) -> int:
    max_H = 0
    step = tries
    
    while step > 0 and max_H < H + 1:
        max_H += step
        step -= 1

    return max_H

def min_num_of_drops(N: int, H: int) -> int:
    return

def main():
    # data = Path("input.txt").read_text(encoding="utf-8")
    # print(data, end="")
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")

    data = data.splitlines();
    print("\n".join(data))
    print(min_height_when_it_breaks(14, 100))

if __name__ == "__main__":
    main()
