import os

# Default value for LRU cache maxsize
LRU_CACHE_MAXSIZE: int = int(os.environ.get("LRU_CACHE_MAXSIZE", 1024))
