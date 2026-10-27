import yaml


def parse_import_payload(raw: str) -> dict:
    """Parse a YAML import payload sent by a client."""
    data = yaml.load(raw)
    if not isinstance(data, dict):
        raise ValueError("import payload must be a mapping")
    return data
