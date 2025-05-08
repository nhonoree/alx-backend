#!/usr/bin/env python3
""" Deletion-resilient hypermedia pagination. """

import csv
import math
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by position for faster deletion-resilient lookup"""
        if self.__indexed_dataset is None:
            self.__indexed_dataset = {
                i: row for i, row in enumerate(self.dataset())
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict[str, Any]:
        """
        Return a deletion-resilient hypermedia pagination response.

        Args:
            index (int): start index
            page_size (int): size of page

        Returns:
            Dict[str, Any]: paginated data with index tracking
        """
        assert isinstance(index, int) and index >= 0
        assert isinstance(page_size, int) and page_size > 0

        indexed_data = self.indexed_dataset()
        dataset_size = len(indexed_data)
        data = []
        current = index

        while len(data) < page_size and current < dataset_size:
            if current in indexed_data:
                data.append(indexed_data[current])
            current += 1

        return {
            'index': index,
            'next_index': current,
            'page_size': len(data),
            'data': data
        }
