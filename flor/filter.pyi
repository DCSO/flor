# DCSO - Flor
# Copyright (c) 2016, 2017, DCSO GmbH. All rights reserved.

from typing import IO, List

magic_seed : bytes

class BloomFilter(object):

    class CapacityError(BaseException): ...

    def __init__(self, n : int, p : float) -> None:
        self.p : float
        self.n : int
        self.N : int
        self.m : int
        #we work in 64 bit blocks as this is the format of the Go filter.
        self.M : int
        self.k : int
        self._bytes : bytes

    def __contains__(self, value : bytes) -> bool: ...

    def read(self, input_file : IO[bytes]) -> None: ...

    def write(self, output_file :IO[bytes]) -> None: ...

    def add(self, value : bytes) -> None: ...

    def check(self, value : bytes) -> bool: ...

    def fingerprint(self, value : bytes) -> List[int]: ...
