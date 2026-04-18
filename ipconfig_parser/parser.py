from config import HOST_MAPPING, ADAPTER_MAPPING, LIST_FIELDS, BAD_GATEWAYS

def normalize_key(key: str, mode: str) -> str:
    key = key.lower().strip()
    key = key.split(".")[0].strip()
    key = " ".join(key.split())

    mapping = HOST_MAPPING if mode == "host" else ADAPTER_MAPPING
    return mapping.get(key, key.replace(" ", "_"))

def clean_value(value: str) -> str:
    return value.split("(")[0].strip()

def is_multiline_value(line: str) -> bool:
    return ". . ." not in line and ":" not in line.split(" ")[0]

def _create_adapter(adapter_name: str) -> dict:
    return      {
                "adapter_name": adapter_name,
                "description": "",
                "physical_address": "",
                "dhcp_enabled": "",
                "autoconfiguration_enabled": "",

                "ipv4_address": "",
                "ipv6_address": "",
                "ipv6_temporary": "",
                "ipv6_link_local": "",

                "subnet_mask": "",
                "default_gateway": [],

                "dhcp_server": "",

                "lease_obtained": "",
                "lease_expires": "",

                "dns_servers": [],
                "dns_suffix": "",

                "dhcpv6_iaid": "",
                "dhcpv6_duid": "",

                "media_state": "",
                "netbios_over_tcpip": "",
                }

def _create_host() -> dict:
    return      {
                "host_name": "",
                "primary_dns_suffix": "",
                "node_type": "",
                "ip_routing_enabled": "",
                "wins_proxy_enabled": "",
                "dns_search_list": "",
                }

def parse_host(host_lines: list[str]) -> dict:
    host = _create_host()

    for line in host_lines:
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = normalize_key(key, "host")
        value = clean_value(value)

        if key in host:
            host[key] = value

    return host

def parse_devices_from_file(file: str) -> dict:
    devices: list[dict] = []
    host_lines: list[str] = []

    current_device: dict | None = None
    current_key: str | None = None
    host_finished = False

    for raw_line in file.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if "windows ip configuration" in line.lower():
            current_device = None
            continue

        # ADAPTERS
        if line.lower().endswith(":") and "adapter" in line.lower():
            host_finished = True

            adapter_name = line.rsplit(":", 1)[0].strip()
            current_device = _create_adapter(adapter_name)
            devices.append(current_device)
            current_key = None
            continue

        # HOSTS
        if current_device is None and not host_finished:
            if ":" in line:
                host_lines.append(line)
            continue

        if current_device is None:
            continue

        # MULTILINE VALUES (DNS, gateway)
        if current_key and current_key in LIST_FIELDS:
            if ". . ." not in line:
                value = clean_value(line)
                if value and value not in BAD_GATEWAYS:
                    current_device[current_key].append(value)
                continue

        # KEY : VALUE
        if ":" in line:
            key, value = line.split(":", 1)
            key = normalize_key(key, "adapter")
            value = clean_value(value)
            current_key = key

            # LIST FIELDS
            if key in LIST_FIELDS:
                if value:
                    current_device[key].append(value)
                continue

            # IPV6 FIELDS
            if key.startswith("ipv6_"):
                current_device[key] = value
                continue

            # NORMAL FIELDS
            current_device[key] = value
            continue

    host = parse_host(host_lines)
    return {"host": host, "adapters": devices}