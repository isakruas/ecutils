import hashlib
from functools import lru_cache


@lru_cache(maxsize=1024, typed=True)
def calculate_file_hash(file_name: str, block_size: int = 16384) -> int:
    """Calculates the SHA-256 hash of a file efficiently.

    This function efficiently calculates the SHA-256 hash of a file, using a cache
    to store previously calculated hashes and a block-wise reading approach to
    optimize memory usage.

    Args:
        file_name (str): The name of the file to calculate the hash for.
        block_size (int, optional): The size of the data blocks to read from the
            file in bytes. Defaults to 16384.

    Returns:
        int: The SHA-256 hash of the file represented as an integer (base 16).

    Raises:
        FileNotFoundError: If the specified file is not found.
    """

    try:
        sha256_hash = hashlib.sha256()
        with open(file_name, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                sha256_hash.update(block)
        return int(sha256_hash.hexdigest(), 16)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_name}") from e
