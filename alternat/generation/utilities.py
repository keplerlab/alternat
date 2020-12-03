import json, os


def save_json_to_disk(dir_path: str, result: dict, rel_path: str):
    """Saves JSON object in a JSON file on disk.

    :param dir_path: Path to directory where result needs to be saved.
    :type dir_path: str
    :param result: Data to be written in the JSON file.
    :type result: dict
    :param rel_path: Relative path to file.
    :type rel_path: str
    """

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(rel_path, "w") as f:
        json.dump(result, f)
