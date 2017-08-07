# DCSO - Flor
# Copyright (c) 2016, 2017, DCSO GmbH. All rights reserved.

import unittest
import math

from io import BytesIO
from flor.filter import BloomFilter

class TestFilter(unittest.TestCase):

    def test_creation(self):
        bf = BloomFilter(n=100000, p=0.01)
        assert bf.n == 100000
        assert bf.p == 0.01
        assert bf.m == 958505
        #we work in 64 bit blocks as this is the format of the Go filter.
        assert bf.M == int(math.ceil(bf.m/64.0))*8 
        assert bf.k == 7
        assert bf.N == 0

    def test_add_and_check(self):
        bf = BloomFilter(n=100000, p=0.01)
        values = (b'bar', b'baz', b'boo', b'bam')
        for value in values:
            bf.add(value)

        assert bf.N == len(values)

        #repeatedly inserting the same values should not increase the count
        for value in values:
            bf.add(value)

        assert bf.N == len(values)

        for value in values:
            assert value in bf

            #this might occasionally fail (very seldom though)
            assert not value+b'sdfsfds2asd' in bf

    def test_read_and_write(self):
        fs = BytesIO()

        bf = BloomFilter(n=100000, p=0.01, data=b'foobar')
        values = (b'bar', b'baz', b'boo', b'bam')
        for value in values:
            bf.add(value)

        bf.write(fs)

        assert len(fs.getvalue()) > 0

        new_bf = BloomFilter(n=1,p=0.1)

        #we rewind the file to the beginning
        fs.seek(0)

        new_bf.read(fs)

        assert new_bf.n == bf.n
        assert new_bf.p == bf.p
        assert new_bf.k == bf.k
        assert new_bf.m == bf.m
        assert new_bf.N == bf.N
        assert new_bf.M == bf.M
        assert new_bf.data == bf.data
        assert new_bf.bytes == bf.bytes

        for value in values:
            assert value in new_bf and value in bf
            assert not value+b'343243' in bf

if __name__ == '__main__':
    unittest.main()