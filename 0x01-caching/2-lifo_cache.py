#!/usr/bin/env python3
""" LIFOCache module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO caching system """

    def __init__(self):
        """ Initialize LIFO cache """
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """ Add an item using LIFO policy """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    discarded = self.stack.pop()
                    del self.cache_data[discarded]
                    print(f"DISCARD: {discarded}")
            self.cache_data[key] = item
            self.stack.append(key)

    def get(self, key):
        """ Retrieve an item """
        return self.cache_data.get(key, None)
