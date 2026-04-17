from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")
ENCODINGS = ["utf-8-sig","utf-8","utf-16","utf-16-le","utf-16-be","cp1250","cp1251","cp1252","cp1254","latin-1","iso-8859-2","iso-8859-1","iso-8859-15","cp850","cp852","cp437","mac_roman","koi8-r","shift_jis","gbk","utf-32"] # most common encodings

def encode_any_file(path: Path, target: str = "utf-8"):
    for enc in ENCODINGS:
        try:
            text = path.read_text(encoding=enc).replace("\ufeff", "")
            path.write_text(text, encoding=target)
            return enc
        except UnicodeDecodeError:
            pass

    raise ValueError("Decode failed!")

def get_txt_files(base_dir: Path):
    return list(base_dir.rglob("*.txt"))

def parse_devices_from_file(file: str):
    devices = {}
    current_device = None

    for line in file.splitlines():
        line = line.strip()

        # searching for a device
        if line.endswith(":") and "adapter" in line.lower():
            current_device = line[:-1]
            devices[current_device] = {}
            continue

        # creating dictionaries for the device's properties and its key-value pairs
        if ":" in line and current_device:
            key, value = line.split(":", 1)
            key = key.strip().replace(".", "")
            value = value.strip()

            devices[current_device][key] = value

    return devices

def console_print(data):
    for device, properties in data.items():
        print(f"\n{device}")
        print("-" * len(device))

        width = max(len(k) for k in properties)

        for k, v in properties.items():
            print(f"{k:<{width}} │ {v}")

def main():
    BASE_DIR = Path(__file__).resolve().parent

    files = get_txt_files(BASE_DIR)

    for file in files:
        enc = encode_any_file(file)
        data = file.read_text(encoding="utf-8", errors="replace")

        print(f"{file.name} -> {enc}")

        devices = parse_devices_from_file(data)
        console_print(devices)

if __name__ == "__main__":
    main()
