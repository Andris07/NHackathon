from pathlib import Path
import sys
import json

sys.stdout.reconfigure(encoding="utf-8")
ENCODINGS = ["utf-8-sig","utf-8","utf-16","utf-16-le","utf-16-be","cp1250","cp1251","cp1252","cp1254","latin-1","iso-8859-2","iso-8859-1","iso-8859-15","cp850","cp852","cp437","mac_roman","koi8-r","shift_jis","gbk","utf-32"] # most common encodings

def read_file_safely(path: Path) -> str:
    for enc in ENCODINGS:
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return path.read_text(encoding="utf-8", errors="replace")

def get_txt_files(base_dir: Path):
    return list(base_dir.rglob("*.txt"))

def normalize_key(key: str) -> str:
    key = key.lower().strip()
    key = key.split(".")[0].strip()
    key = " ".join(key.split())

    mapping =                   {
                                "physical address": "physical_address",
                                "ipv4 address": "ipv4_address",
                                "autoconfiguration ipv4 address": "ipv4_address",

                                "ipv6 address": "ipv6_address",
                                "temporary ipv6 address": "ipv6_temporary",
                                "link-local ipv6 address": "ipv6_link_local",

                                "subnet mask": "subnet_mask",
                                "default gateway": "default_gateway",
                                "dhcp enabled": "dhcp_enabled",

                                "dns servers": "dns_servers",
                                "connection-specific dns suffix": "dns_suffix",
                                "dns suffix search list": "dns_search_list",

                                "description": "description",
                                }
    return mapping.get(key.strip(), key.strip().replace(" ", "_"))

def parse_devices_from_file(file: str):
    devices = []
    current_device = None
    current_key = None

    ipv6_keys =                 {
                                "ipv6 address": "ipv6_address",
                                "temporary ipv6 address": "ipv6_temporary",
                                "link-local ipv6 address": "ipv6_link_local"
                                }

    for line in file.splitlines():
        line = line.strip()

        # new adapter
        if line.endswith(":") and "adapter" in line.lower():
            current_device =    {
                                "adapter_name": line[:-1],
                                "description": "",
                                "physical_address": "",
                                "dhcp_enabled": "",
                                "ipv4_address": "",
                                "ipv6_address": "",
                                "ipv6_temporary": "",
                                "ipv6_link_local": "",
                                "subnet_mask": "",
                                "default_gateway": [],
                                "dns_servers": [],
                                "dns_suffix": "",
                                "dns_search_list": "",
                                }
            devices.append(current_device)
            current_key = None
            continue

        if not current_device:
            continue

        # adapter key-value pairs
        if ":" in line:
            key, value = line.split(":", 1)
            key = normalize_key(key)
            value = value.strip()
            current_key = key

            # IPv6 types
            if key in ipv6_keys:
                current_device[ipv6_keys[key]] = value.split("(")[0].strip()
                continue

            # description
            if "description" in key:
                current_device["description"] = value
                continue

            # physical address
            if "physical_address" in key:
                current_device["physical_address"] = value
                continue

            # dhcp enabled
            if "dhcp_enabled" in key:
                current_device["dhcp_enabled"] = value
                continue

            # ipv4
            if key == "ipv4_address":
                current_device["ipv4_address"] = value.split("(")[0].strip()
                continue

            # subnet mask
            if key == "subnet_mask":
                current_device["subnet_mask"] = value
                continue

            # dns suffix
            if key == "dns_suffix":
                current_device["dns_suffix"] = value
                continue

            # dns search list
            if key == "dns_search_list":
                current_device["dns_search_list"] = value
                continue

            # default gateway
            if key == "default_gateway":
                if value and value not in ("127.0.0.1", "::1"):
                    current_device["default_gateway"].append(value)
                continue

            # dns servers
            if key == "dns_servers":
                if value:
                    current_device["dns_servers"].append(value)
                continue

            continue

        # multiline values (default_gateway, dns_servers)
        if current_key and line:
            if current_key == "default_gateway":
                if line not in ("127.0.0.1", "::1"):
                    current_device["default_gateway"].append(line)
                continue

            elif current_key == "dns_servers":
                current_device["dns_servers"].append(line)
                continue

    return devices

def console_print(devices):
    for device in devices:
        print(f"\n{device['adapter_name']}")
        print("-" * len(device["adapter_name"]))

        for k, v in device.items():
            if k == "adapter_name":
                continue
            print(f"{k:<20} │ {v}")

def export_to_json(file: Path, adapters):
    return  {
            "file_name": file.name,
            "adapters": adapters
            }

def main():
    BASE_DIR = Path(__file__).resolve().parent
    files = get_txt_files(BASE_DIR)
    results = []

    for file in files:
        data = read_file_safely(file)

        adapters = parse_devices_from_file(data)

        results.append(export_to_json(file, adapters))

        print(f"{file.name}")
        console_print(adapters)

    with open(BASE_DIR / "adapters.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
