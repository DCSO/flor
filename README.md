# Flor - A Bloom filter implementation in Python

Flor implements a Bloom filter class that is fully compatible with our
[Go Bloom filter implementation](https://github.com/DCSO/bloom).

# Requirements

Flor is compatible with Python 2 and Python 3 and does not require any
non-standard modules.

# Installation

Flor can be installed via PyPi/pip:

    pip install flor

Alternatively, you can install it from source:

    git clone https://github.com/DCSO/flor.git
    cd flor

    #add "sudo" if you're not in a virtual environment
    python setup.py install

# Usage

Creating a new Bloom filter:

    from flor import BloomFilter

    bf = BloomFilter(n=100000, p=0.001)

    bf.add(b"foo")
    bf.add(b"bar")
    bf.add(b"baz")

    b"baz" in bf #returns True
    b"nope" in bf #returns False

Writing a Bloom filter to a file:

    bf = BloomFilter()
    with open('test.bloom', 'wb') as f:
        bf.write(f)

Reading a Bloom filter from a file:

    bf = BloomFilter()
    with open('test.bloom', 'rb') as f:
        bf.read(f)

The binary format of the filter is compatible with that generated by our Go library, so you can use the two interchangeably.

# License

Flor is licensed under the BSD 3 Clause license (see LICENSE).