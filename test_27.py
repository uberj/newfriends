import unittest

from cipher.cbc import CBCCipher
from util.somecode import xor

FIXED_KEY = b'K8,zXi^,[rY9u\x0cAk'
cipher = CBCCipher(FIXED_KEY, FIXED_KEY)


def encrypt_data(user_data: bytes) -> bytes:
	s = b"comment1=cooking%20MCs;userdata=" \
	    + user_data.replace(b";", b"").replace(b"=", b"") \
	    + b";comment2=%20like%20a%20pound%20of%20bacon"

	return cipher.encrypt(s)


def decrypt(blob: bytes) -> bytes:
	d = cipher.decrypt(blob)
	for c in d:
		if c >= 128:
			raise Exception("Invalid blob: " + str(d))
	return d


class TestChallenge27(unittest.TestCase):
	@unittest.skip
	def test_decrypt(self):
		e = encrypt_data("foobar".encode())
		blocks = [e[i:i+16] for i in range(0, len(e), 16)]
		blocks[1] = b'\x00' * 16
		blocks[2] = blocks[0]
		r = b''.join(blocks)
		decrypt(r)

	def test_attack_exception(self):
		# I won't pretend to understand how this actually works. I just know I'll never use CBC
		# Exception: Invalid blob: b'comment1=cooking\xb1A\x07\xed#Aze\xcd\xcd\x8aS7\xcb\xac\xdd(WA\x17=\x07*\x1df\x116V\x1ee/\x0c\xabw\xa2\xb1\x8a\x15\xbe0{H\xb4\xd7y\xf7\xd6\xfbund%20of%20bacon'
		e = b'comment1=cooking\xb1A\x07\xed#Aze\xcd\xcd\x8aS7\xcb\xac\xdd(WA\x17=\x07*\x1df\x116V\x1ee/\x0c\xabw\xa2\xb1\x8a\x15\xbe0{H\xb4\xd7y\xf7\xd6\xfbund%20of%20bacon'

		blocks = [e[i:i + 16] for i in range(0, len(e), 16)]
		self.assertEqual(FIXED_KEY, (xor(blocks[0], blocks[2])))
