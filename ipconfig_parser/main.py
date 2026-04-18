from pathlib import Path
import sys
import json

from config import ENCODINGS
from parser import parse_devices_from_file
from filterFields import filter_adapter, filter_host

sys.stdout.reconfigure(encoding="utf-8")

def get_txt_files(base_dir: Path):
    return list(base_dir.rglob("*.txt"))

def read_file_safely(path: Path) -> str:
    for enc in ENCODINGS:
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return path.read_text(encoding="utf-8", errors="replace")

def export_to_json(data, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    BASE_DIR = Path(__file__).resolve().parent

    files = sorted(get_txt_files(BASE_DIR), key=lambda f: f.name)
    data = []

    for file in files:
        file_content = read_file_safely(file)
        parsed = parse_devices_from_file(file_content)

        filtered_adapters = [filter_adapter(a) for a in parsed["adapters"]]
        filtered_host = filter_host(parsed["host"])

        data.append({"file_name": file.name, "adapters": filtered_adapters})

    output_file = BASE_DIR / "devices.json"
    export_to_json(data, output_file)

    print(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
