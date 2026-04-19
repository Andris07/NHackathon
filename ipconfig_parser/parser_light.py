from config import ADAPTER_MAPPING, LIST_FIELDS
from parser import clean_value

def normalize_key(key: str, mapping: dict) -> str:
    key = key.lower().split(".", 1)[0].strip()
    return mapping.get(key, key.replace(" ", "_"))

def _create_adapter(adapter_name: str) -> dict:
    return      {
                "adapter_name": adapter_name,
                "description": "",
                "physical_address": "",
                "dhcp_enabled": "",
                "ipv4_address": "",
                "subnet_mask": "",
                "default_gateway": "",
                "dns_servers": [],
                }

def parse_adapters_from_file(file: str) -> dict:
    adapters = []
    current_adapter = None
    current_key = None

    for raw_line in file.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        clean = line.lower()

        # ADAPTERS
        if clean.endswith(":") and "adapter" in clean:
            adapter_name = line.rsplit(":", 1)[0].strip()
            current_adapter = _create_adapter(adapter_name)
            adapters.append(current_adapter)
            current_key = None
            continue

        if current_adapter is None:
            continue

        # MULTILINE VALUES (DNS, gateway)
        if current_key in LIST_FIELDS:
            if ". . ." not in line:
                value = clean_value(line, current_key)
                if value:
                    current_adapter[current_key].append(value)
                continue

        # KEY : VALUE
        if ":" in line:
            key, value = line.split(":", 1)
            key = normalize_key(key, ADAPTER_MAPPING)
            value = clean_value(value, key)
            current_key = key

            # LIST FIELDS
            if key in LIST_FIELDS:
                if value:
                    current_adapter[key].append(value)
                continue

            # NORMAL FIELDS
            current_adapter[key] = value

    return {"adapters": adapters}