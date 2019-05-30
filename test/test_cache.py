
import unittest

from TomoriNao.cache import Cache


class TestCache(unittest.TestCase):

    def test_constructor(self):
        cache = Cache()
        self.assertEqual(cache.size, 8)
        cache = Cache(16)
        self.assertEqual(cache.size, 16)
        with self.assertRaises(ValueError):
            Cache(0)
        with self.assertRaises(ValueError):
            Cache(-1)

    def test_append(self):
        cache = Cache()
        for i in range(4):
            cache.append(i)
        self.assertEqual(len(cache), 4)
        for i in range(4):
            cache.append(i)
        self.assertEqual(len(cache), 8)
        for i in range(4):
            cache.append(i)
        self.assertEqual(len(cache), 8)    # cache still has four elements
        for i in range(10, 18):
            cache.append(i)
        self.assertEqual(cache, list(range(10, 18)))     # cache should be completely overwritten
