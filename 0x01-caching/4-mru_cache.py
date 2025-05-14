#!/usr/bin/env python3
"""MRUCache module"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache class that inherits from BaseCaching"""

    def __init__(self):
        """Initialize the cache"""
        super().__init__()
        self.mru_keys = []

    def put(self, key, item):
        """Assign the item value to key in the cache"""
        if key is None or item is None:
            return

        # If the key already exists, remove it so we can update its position later
        if key in self.cache_data:
            self.mru_keys.remove(key)

        self.cache_data[key] = item
        self.mru_keys.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Remove the most recently used key (last in list before the new one)
            mru_key = self.mru_keys[-2]
            del self.cache_data[mru_key]
            self.mru_keys.remove(mru_key)
            print(f"DISCARD: {mru_key}")

    def get(self, key):
        """Return the value linked to key, or None"""
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end to mark it as most recently used
        self.mru_keys.remove(key)
        self.mru_keys.append(key)

        return self.cache_data[key]
