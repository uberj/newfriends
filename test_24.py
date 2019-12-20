import unittest
import random

from cipher.MersenneTwisterCipher import MersenneTwisterCipher
from util.somecode import rand_n_string

R = random.Random()
rint = lambda: R.randint(0, 2 ** 32 - 1)
N = 624


class TestChallenge24(unittest.TestCase):
	def test_mt_cipher_round_trip(self):
		cipher = MersenneTwisterCipher(rint())
		s = rand_n_string(10000).encode()
		e = cipher.encrypt(s)
		d = cipher.decrypt(e)
		self.assertEqual(s, d)

	def test_infer_secret(self):
		secret = R.randint(0, 2**8)  # using an 8 bit seed to make the exercise more time friendly
		cipher = MersenneTwisterCipher(secret)
		s = rand_n_string(R.randint(10, 40)).encode() + b"A" * 14
		e = cipher.encrypt(s)
		attack_string = b"A" * len(s)
		for i in range(2**32):
			cipher = MersenneTwisterCipher(i)
			e_attack = cipher.encrypt(attack_string)
			if e_attack.endswith(e[-14:]):
				self.assertEqual(secret, i)
				return

		self.fail("Didn't find the secret")


