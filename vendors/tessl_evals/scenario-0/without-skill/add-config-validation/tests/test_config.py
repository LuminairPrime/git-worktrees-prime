import json
import tempfile
import os
from src.config import load_config


def test_load_simple_config():
    data = {"host": "localhost", "port": 5432}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        path = f.name
    try:
        result = load_config(path)
        assert result == data
    finally:
        os.unlink(path)
