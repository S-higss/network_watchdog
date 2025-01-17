# toml configファイル読み込み用モジュール

from typing import Any
import toml

def load_config(config_path) -> dict[str, Any]:
    config = toml.load(config_path)
    return config