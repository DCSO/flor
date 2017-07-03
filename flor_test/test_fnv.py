# DCSO - Flor
# Copyright (c) 2016, 2017, DCSO GmbH. All rights reserved.

import unittest
from flor.fnv import fnv_1, fnv_1a

class TestFNV(unittest.TestCase):

    def test_fnv_1(self):
        assert fnv_1(b"test") == 0x8c093f7e9fccbf69

    def test_fnv_1a(self):
        assert fnv_1a(b"test") == 0xf9e6e6ef197c2b25

if __name__ == '__main__':
    unittest.main()