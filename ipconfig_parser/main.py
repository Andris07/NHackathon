from pathlib import Path
import sys
import json

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

        # adapter
        if line.endswith(":") and "adapter" in line.lower():
            current_device =    {
                                "adapter_name": line[:-1],
                                "description": "",
                                "physical_address": "",
                                "dhcp_enabled": "",
                                "ipv4_address": "",
                                "subnet_mask": "",
                                "default_gateway": "",
                                "dns_servers": "",
                                }
            devices.append(current_device)
            continue

        # adapter details
        if ":" in line and current_device:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            # mapping ipconfig keys
            if "description" in key:
                current_device["description"] = value
            elif "physical address" in key:
                current_device["physical_address"] = value
            elif "dhcp enabled" in key:
                current_device["dhcp_enabled"] = value
            elif "ipv4 address" in key:
                current_device["ipv4_address"] = value.split("(")[0].strip()
            elif "subnet mask" in key:
                current_device["subnet_mask"] = value
            elif "default gateway" in key:
                current_device["default_gateway"] = value
            elif "dns servers" in key:
                current_device["dns_servers"] = [v.strip() for v in value.split() if v]

    return devices

def export_to_json(file: Path, adapters):
    return
    {
        "file_name": file.name,
        "adapters": adapters
    }

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
