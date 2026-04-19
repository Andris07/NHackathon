from pathlib import Path
import sys
import json

from main import get_txt_files, read_file_safely, export_to_json
from parser_light import parse_adapters_from_file
from filterFields import filter_adapter

sys.stdout.reconfigure(encoding="utf-8")

def main():
    BASE_DIR = Path(__file__).resolve().parent

    files = sorted(get_txt_files(BASE_DIR), key=lambda f: f.name)
    data = []

    for file in files:
        file_content = read_file_safely(file)
        parsed = parse_adapters_from_file(file_content)

        filtered_adapters = [filter_adapter(a) for a in parsed["adapters"]]

        data.append({"file_name": file.name, "adapters": filtered_adapters})

    output_file = BASE_DIR / "devices.json"
    export_to_json(data, output_file)

    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
