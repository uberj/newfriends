import unittest
from crypto.sha1 import sha1

from util.bettercode import seal_sha1, random_word, confirm_seal_sha1
from util.somecode import rand_n_string


class TestChallenge28(unittest.TestCase):
	def test_sha1(self):
		self.assertEqual(sha1(b""), b'da39a3ee5e6b4b0d3255bfef95601890afd80709')
		self.assertEqual(sha1(b"The quick brown fox jumps over the lazy dog"), b'2fd4e1c67a2d28fced849ee1bb76e7391b93eb12')

	def test_sha1_seal(self):
		secret = random_word()
		seal = seal_sha1(secret, b"foobar")
		self.assertFalse(confirm_seal_sha1(secret, seal, b"foobarr"))
		self.assertTrue(confirm_seal_sha1(secret, seal, b"foobar"))

	@unittest.skip
	def test_sha1_message_length(self):
		n_string = rand_n_string(100).encode()
		h = seal_sha1(random_word(), n_string)
		# https://en.wikipedia.org/wiki/SHA-1#SHA-1_pseudocode
		# ml = message length in bits (always a multiple of the number of bits in a character).
		# append ml, the original message length, as a 64-bit big-endian integer. #    Thus, the total length is a multiple of 512 bits.
		ml = int.from_bytes(h[-8:], 'big')
		print(ml)
