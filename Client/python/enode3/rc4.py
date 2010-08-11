"""Instructional implementation of Ron's Cipher #4 (AKA RC4).
Follows form of a `Programming Praxis exercise`_.
 
.. _Programming Praxis exercise:
http://programmingpraxis.com/2009/09/04/rons-cipher-4/
 
:author: Christopher D. Leary <cdleary@gmail.com>
:modified: Gabriel Caraballo <eibriel@yahoo.com.ar>
"""

class rc4:
    def __init__(self):
        pass

    def initialize(self, key):
        """Produce a 256-entry list based on `key` (a sequence of numbers)
    as the first step in RC4.
    Note: indices in key greater than 255 will be ignored.
    """
        key = [ord(char) for char in key]
        k = range(256)
        j = 0
        for i in range(256):
            j = (j + k[i] + key[i % len(key)]) % 256
            k[i], k[j] = k[j], k[i]
        self.k = k
        return k
     
     
    def _gen_random_bytes(self, k):
        """Yield a pseudo-random stream of bytes based on 256-byte array `k`."""
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + k[i]) % 256
            k[i], k[j] = k[j], k[i]
            yield k[(k[i] + k[j]) % 256]

    def run_rc4(self, k, text, ty=0):

        cipher_chars = []
        random_byte_gen = self._gen_random_bytes( list ( k ) )
        for char in text:
            byte = ord(char)
            cipher_byte = byte ^ random_byte_gen.next()
            cipher_chars.append(chr(cipher_byte))
        return ''.join(cipher_chars)
