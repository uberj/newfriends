from typing import Callable

from crypto.sha1 import sha1
from util.somecode import xor
from binascii import unhexlify


def hmac_sha1(key: bytes, message: bytes):
	return hmac(key, message, sha1, 64)


def hmac(key: bytes, message: bytes, hash: Callable[[bytes], bytes], block_size):
	"""
	function hmac is
    input:
        key:        Bytes     // Array of bytes
        message:    Bytes     // Array of bytes to be hashed
        hash:       Function  // The hash function to use (e.g. SHA-1)
        blockSize:  Integer   // The block size of the underlying hash function (e.g. 64 bytes for SHA-1)
        outputSize: Integer   // The output size of the underlying hash function (e.g. 20 bytes for SHA-1)

    // Keys longer than blockSize are shortened by hashing them
    if (length(key) > blockSize) then
        key ← hash(key) // Key becomes outputSize bytes long

    // Keys shorter than blockSize are padded to blockSize by padding with zeros on the right
    if (length(key) < blockSize) then
        key ← Pad(key, blockSize) // Pad key with zeros to make it blockSize bytes long

    o_key_pad ← key xor [0x5c * blockSize]   // Outer padded key
    i_key_pad ← key xor [0x36 * blockSize]   // Inner padded key

    return hash(o_key_pad ∥ hash(i_key_pad ∥ message)) // Where ∥ is concatenation

    ^ From https://en.wikipedia.org/wiki/HMAC#Implementation
	"""

	if len(key) > block_size:
		key = hash(key)

	if len(key) < block_size:
		key = key.ljust(block_size, b"\x00")

	assert len(key) == block_size
	o_key_pad = xor(key, b'\x5C' * block_size)
	i_key_pad = xor(key, b'\x36' * block_size)

	b = unhexlify(hash(i_key_pad + message))
	return hash(o_key_pad + b)
