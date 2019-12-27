import unittest

import binascii
import struct
from util.bettercode import seal_md4, random_word, confirm_seal_md4
from crypto.md4 import md4, md4_restart, md4_pad


class TestChallenge30(unittest.TestCase):
	def test_consistent_behavior(self):
		message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
		s1 = md4(message)

		# now see if we can reconstruct
		A, B, C, D = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476)
		ml = len(message)
		s2 = md4_restart(message, ml, A, B, C, D)

		self.assertEqual(s1, s2)

	@unittest.skip
	def test_observe_md4(self):
		for i in range(1000):
			m1 = md4(b"f"* i)
			blocks = [m1[i:i+8] for i in range(0, 8 * 4, 8)]
			print(blocks)



	def test_forgery(self):
		secret = random_word()
		msg_to_attack = b"comment1=cooking%20MCs;comment2=%20like%20a%20pound%20of%20bacon;userdata=foo"
		seal = seal_md4(secret, msg_to_attack)

		# Get the previous state of the function
		blocks = [seal[i:i+8] for i in range(0, len(seal), 8)]
		self.assertEqual(seal, b''.join(blocks))
		A, B, C, D = struct.unpack('<IIII', binascii.unhexlify(seal))

		# We have to guess the pad length
		for i in range(400):
			key_guess = b'X' * i
			p = md4_pad(key_guess + msg_to_attack)
			extra = b";admin=true;"
			original_byte_len = len(key_guess) + len(msg_to_attack) + len(p) + len(extra)

			s2 = md4_restart(extra, original_byte_len, A, B, C, D)

			false_msg = msg_to_attack + p + extra
			if confirm_seal_md4(secret, s2, false_msg):
				self.assertTrue("True", "We found a winner!")
				return

		self.fail("No solution")



