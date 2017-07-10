# DCSO - Flor
# Copyright (c) 2016, 2017, DCSO GmbH. All rights reserved.

offset = 14695981039346656037
prime = 1099511628211

def fnv_1(value):
    if not isinstance(value, bytes):
        raise TypeError("Value must be a bytes object!")
    hash = offset
    for byte in bytearray(value):
        hash = (hash*prime) & 0xFFFFFFFFFFFFFFFF
        hash ^= byte
    return hash

def fnv_1a(value):
    if not isinstance(value, bytes):
        raise TypeError("Value must be a bytes object!")
    hash = offset
    for byte in bytearray(value):
        hash ^= byte
        hash = (hash*prime) & 0xFFFFFFFFFFFFFFFF
    return hash

