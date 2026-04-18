from config import IMPORTANT_FIELDS

def filter_adapter(adapter: dict) -> dict:
    filtered = {}

    for key in IMPORTANT_FIELDS:
        value = adapter.get(key, "")

        if key in ("default_gateway", "dns_servers"):
            filtered[key] = value if isinstance(value, list) else []
        else:
            filtered[key] = value if value else ""

    return filtered

def filter_host(host: dict) -> dict:
    return host