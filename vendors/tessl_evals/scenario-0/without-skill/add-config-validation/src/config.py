"""Configuration loader for the backend service."""


def load_config(path: str) -> dict:
    """Load a JSON config from the given file path."""
    import json
    with open(path) as f:
        return json.load(f)
