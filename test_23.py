import unittest
import random
from cipher.MersenneTwisterPRNG import MersenneTwisterPRNG

R = random.Random()
rint = lambda: R.randint(0, 2 ** 32 - 1)
N = 624

def rebuild_state(prng: MersenneTwisterPRNG) -> [int]:
	state = []
	for i in range(N):
		rn = prng.next()
		temper = MersenneTwisterPRNG.invert_temper(rn)
		state.append(temper)

	return state


class TestChallenge23(unittest.TestCase):
	def test_break_the_twister(self):
		original = MersenneTwisterPRNG(rint())
		mTState = rebuild_state(original)

		rebuilt = MersenneTwisterPRNG(0)
		rebuilt.load_state(mTState)

		for i in range(4 * N):
			original_next = original.next()
			rebuilt_next = rebuilt.next()
			self.assertEqual(original_next, rebuilt_next)

	def test_invert_temper(self):
		prng = MersenneTwisterPRNG(rint())
		i = rint()
		temper = prng.temper(i)
		untemper = prng.invert_temper(temper)
		self.assertEqual(bin(untemper), bin(i))

	def test_bit_slice(self):
		x = int("1111" + "0" * 7 + "1" * 7 + "0" * 7 + "1" * 7, 2)
		self.assertEqual(bin(int("1" * 7, 2)), bin(MersenneTwisterPRNG.bit_slice(x, 0, 7)))
		self.assertEqual(bin(int("0" * 7, 2)), bin(MersenneTwisterPRNG.bit_slice(x, 1, 7)))
		self.assertEqual(bin(int("1" * 7, 2)), bin(MersenneTwisterPRNG.bit_slice(x, 2, 7)))
		self.assertEqual(bin(int("0" * 7, 2)), bin(MersenneTwisterPRNG.bit_slice(x, 3, 7)))
		self.assertEqual(bin(int("1" * 4, 2)), bin(MersenneTwisterPRNG.bit_slice(x, 4, 7)))

	def test_invert_right_shift_zero_and(self):
		# y_p = y ^ (y >> l)
		y = rint()
		l = 18
		u = 2 ** 32 - 1
		y_p = y ^ (y >> l)
		self.assertEqual(bin(y), bin(MersenneTwisterPRNG.invert_right_shift(y_p, l, u)))

	def test_invert_right_shift(self):
		# y_p = y ^ ((y >> l) & u)
		y = random.Random().randint(0, (2 ** 32) - 1)
		u = int("FFFFFFFF", 16)
		l = 11
		y_p = y ^ ((y >> l) & u)
		self.assertEqual(y, MersenneTwisterPRNG.invert_right_shift(y_p, l, u))

	def test_invert_left_shift(self):
		# y_p = y ^ ((y << l) & u)
		y = random.Random().randint(0, (2 ** 32) - 1)
		u = int("9D2C5680", 16)
		l = 7
		y_p = y ^ ((y << l) & u)
		self.assertEqual(y, MersenneTwisterPRNG.invert_left_shift(y_p, l, u))
