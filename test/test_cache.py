
import unittest

from naotomori.cache import Cache


class TestCache(unittest.TestCase):

    def test_constructor(self):
        cache = Cache()
        self.assertEqual(cache.size, 16)
        cache = Cache(32)
        self.assertEqual(cache.size, 32)
        with self.assertRaises(ValueError):
            Cache(0)
        with self.assertRaises(ValueError):
            Cache(-1)

    def test_append(self):
        cache = Cache()
        for i in range(8):
            cache.append(i)
        self.assertEqual(len(cache), 8)
        for i in range(8):
            cache.append(i)
        self.assertEqual(len(cache), 16)
        for i in range(8):
            cache.append(i)
        self.assertEqual(len(cache), 16)    # cache still has 16 elements
        for i in range(16, 32):
            cache.append(i)
        self.assertEqual(cache, list(range(16, 32)))     # cache should be completely overwritten
