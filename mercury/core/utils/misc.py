import json
import os
from typing import Any, List


def load_secrets(file_path: str) -> None:
    """
    Loads secrets from a JSON file and sets them as environment variables.

    Parameters:
    - file_path (str): The path to the JSON file containing the secrets.
    """
    try:
        with open(file_path) as f:
            config = json.load(f)
            for key, value in config.items():
                os.environ[key] = value
        print("Loaded secrets!")
    except:
        print(
            "Failed loading secrets! If keys are already environment variables this is fine :)"
        )
