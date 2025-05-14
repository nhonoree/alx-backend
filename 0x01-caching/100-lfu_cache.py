#!/usr/bin/env python3
""" LFUCache module """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class inherits from BaseCaching and implements LFU caching """

    def __init__(self):
        """Initialize the LFU cache"""
        super().__init__()
        self.freq = {}  # Track frequency of keys
        self.usage_order = []  # Track usage order to resolve LRU tie

    def put(self, key, item):
        """Add an item to the cache using LFU + LRU policy"""
        if key is None or item is None:
            return

        # If key already exists, just update value and frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            self._update_usage(key)
            return

        # If we need to evict an item
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Find the min frequency
            min_freq = min(self.freq.values())
            # Get keys with that frequency
            keys_with_min_freq = [k for k in self.freq if self.freq[k] == min_freq]
            # If more than one, use LRU: evict the one least recently used
            for k in self.usage_order:
                if k in keys_with_min_freq:
                    discarded = k
                    break
            # Remove discarded key
            del self.cache_data[discarded]
            del self.freq[discarded]
            self.usage_order.remove(discarded)
            print(f"DISCARD: {discarded}")

        # Add the new item
        self.cache_data[key] = item
        self.freq[key] = 1
        self.usage_order.append(key)

    def get(self, key):
        """Return the value linked to key, or None"""
        if key is None or key not in self.cache_data:
            return None

        self.freq[key] += 1
        self._update_usage(key)
        return self.cache_data[key]

    def _update_usage(self, key):
        """Move key to end of usage_order to mark it as most recently used"""
        if key in self.usage_order:
            self.usage_order.remove(key)
        self.usage_order.append(key)
