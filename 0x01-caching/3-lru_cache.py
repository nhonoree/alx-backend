#!/usr/bin/env python3
""" LRUCache module
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRU caching system """

    def __init__(self):
        """ Initialize LRU cache """
        super().__init__()
        self.usage = []

    def put(self, key, item):
        """ Add an item using LRU policy """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.usage.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lru = self.usage.pop(0)
                del self.cache_data[lru]
                print(f"DISCARD: {lru}")
            self.cache_data[key] = item
            self.usage.append(key)

    def get(self, key):
        """ Retrieve an item and update usage """
        if key in self.cache_data:
            self.usage.remove(key)
            self.usage.append(key)
            return self.cache_data[key]
        return None
