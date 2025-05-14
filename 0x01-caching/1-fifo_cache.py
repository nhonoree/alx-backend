#!/usr/bin/env python3
""" FIFOCache module
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO caching system """

    def __init__(self):
        """ Initialize FIFO cache """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item using FIFO policy """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    discarded = self.queue.pop(0)
                    del self.cache_data[discarded]
                    print(f"DISCARD: {discarded}")
                self.queue.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item """
        return self.cache_data.get(key, None)
