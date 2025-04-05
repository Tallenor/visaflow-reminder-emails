from typing import Any, List, Dict, Optional, Union


def safe_get(data: Dict[str, Any], keys: Union[List[str], str], default: Optional[Any] = None) -> Any:
    """
    Safely retrieves a value from a dictionary using either a list of keys
    or a dot-notation string.
    Args:
        data (dict): The dictionary to traverse.
        keys (Union[List[str], str]): A list of keys or a dot-notation string (e.g., "key1.key2.key3").
        default: The value to return if the nested value is not found (default: None).
    Returns:
        The value if found, the specified default value otherwise.
    """
    if isinstance(keys, str):
        keys = keys.split('.')  # Split dot-notation string into a list of keys

    if not isinstance(keys, list):
        raise TypeError("keys must be a list of strings or a dot-notation string")

    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current