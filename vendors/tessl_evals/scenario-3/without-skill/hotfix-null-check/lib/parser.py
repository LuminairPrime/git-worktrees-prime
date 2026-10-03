"""Core parser for dataflow events."""


def parse_event(raw):
    if not isinstance(raw, dict):
        raise ValueError("Event must be a dict")
    return {
        "type": raw.get("type", "unknown"),
        "payload": raw.get("payload", {}),
    }
