# DCSO - Flor
# Copyright (c) 2016, 2017, DCSO GmbH. All rights reserved.

import math
from struct import unpack, pack
from .fnv import fnv_1

magic_seed = b'this-is-magical'

class BloomFilter(object):

    class CapacityError(BaseException):
        pass

    def __init__(self, n=100000, p=0.001):
        self.p = p
        self.n = n
        self.N = 0
        self.m = int(abs(math.ceil(float(n) * math.log(float(p)) / math.pow(math.log(2.0), 2.0))))
        #we work in 64 bit blocks as this is the format of the Go filter.
        self.M = int(math.ceil(float(self.m) / 64.0))*8
        self.k = int(math.ceil(math.log(2) * float(self.m) / float(n)))
        self._bytes = bytearray([0 for i in range(self.M)])

    def __contains__(self, value):
        return self.check(value)

    def read(self, input_file : IO[bytes]):
        bs8 = input_file.read(8)
        if len(bs8) != 8:
            raise IOError("Invalid filter!")
        self.n = unpack('<Q', bs8)[0]

        bs8 = input_file.read(8)
        if len(bs8) != 8:
            raise IOError("Invalid filter!")
        self.p = unpack('<d', bs8)[0]

        bs8 = input_file.read(8)
        if len(bs8) != 8:
            raise IOError("Invalid filter!")
        self.k = unpack('<Q', bs8)[0]

        bs8 = input_file.read(8)
        if len(bs8) != 8:
            raise IOError("Invalid filter!")
        self.m = unpack('<Q', bs8)[0]

        bs8 = input_file.read(8)
        if len(bs8) != 8:
            raise IOError("Invalid filter!")
        self.N = unpack('<Q', bs8)[0]

        self.M = int(math.ceil(self.m/64.0))*8

        self._bytes = bytearray(input_file.read(self.M))
        if len(self._bytes) != self.M:
            raise IOError("Mismatched number of bytes: Expected {}, got {}.".format(self.M,len(self._bytes)))

    def write(self, output_file):
        output_file.write(pack('<Q', self.n))
        output_file.write(pack('<d', self.p))
        output_file.write(pack('<Q', self.k))
        output_file.write(pack('<Q', self.m))
        output_file.write(pack('<Q', self.N))
        output_file.write(bytes(self._bytes))

    def add(self, value):
        fp = self.fingerprint(value)
        new_value = False
        for fpe in fp:
            k = int(fpe / 8)
            l = fpe % 8
            v = 1 << l
            if self._bytes[k] & v == 0:
                new_value = True
            self._bytes[k] |= v
        if new_value:
            self.N+=1
            if self.N >= self.n:
                raise BloomFilter.CapacityError("Bloom filter is full!")

    def check(self, value):
        fp = self.fingerprint(value)
        for fpe in fp:
            k = int(fpe / 8)
            l = fpe % 8
            if self._bytes[k] & (1 << l) == 0:
                return False
        return True

    def fingerprint(self, value):
        bvalue = bytes(value)
        h1 = fnv_1(bvalue)
        h2 = fnv_1(bvalue+magic_seed)

        fp = []

        for i in range(self.k):
            fp.append(((h1+(i+1)*h2) & 0xffffffffffffffff) % self.m)

        return fp
