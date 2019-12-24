import unittest

from util.bettercode import seal_sha1, random_word, confirm_seal_sha1
from crypto.sha1 import sha1, sha1_restart, sha1_pad



class TestChallenge29(unittest.TestCase):
	def test_consistent_behavior(self):
		message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
		s1 = sha1(message)

		# now see if we can reconstruct
		h0 = 0x67452301
		h1 = 0xEFCDAB89
		h2 = 0x98BADCFE
		h3 = 0x10325476
		h4 = 0xC3D2E1F0
		ml = len(message)
		s2 = sha1_restart(message, ml, h0, h1, h2, h3, h4)

		self.assertEqual(s1, s2)

	def test_faker(self):
		message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
		s1 = sha1(message)

	def test_forgery(self):
		secret = random_word()
		msg_to_attack = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
		seal = seal_sha1(secret, msg_to_attack)

		# Get the previous state of the function
		blocks = [seal[i:i+8] for i in range(0, 40, 8)]
		self.assertEqual(seal, b''.join(blocks))
		h0, h1, h2, h3, h4 = map(lambda x: int(x, 16), blocks)

		# We have to guess the pad length
		for i in range(400):
			key_guess = b'X' * i
			p = sha1_pad(key_guess + msg_to_attack)
			extra = b";admin=true;"
			original_byte_len = len(key_guess) + len(msg_to_attack) + len(p) + len(extra)

			s2 = sha1_restart(extra, original_byte_len, h0, h1, h2, h3, h4)

			false_msg = msg_to_attack + p + extra
			if confirm_seal_sha1(secret, s2, false_msg):
				self.assertTrue("True", "We found a winner!")
				return

		self.fail("No solution")



