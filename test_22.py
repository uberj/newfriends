import unittest

from MersenneTwisterPRNG import MersenneTwisterPRNG
import time
import random

r = random.Random()

@unittest.SkipTest
class TestChallenge22(unittest.TestCase):
	def test_stable_output(self):
		r1 = MersenneTwisterPRNG(0)
		a = []
		for i in range(1000):
			a.append(r1.next())

		r2 = MersenneTwisterPRNG(0)
		b = []
		for i in range(1000):
			b.append(r2.next())

		self.assertEquals(a, b)

	def test_wait_test(self):
		print("Start: " + str(int(time.time())))
		time.sleep(r.randint(40, 100))
		prng = MersenneTwisterPRNG(int(time.time()))
		print(prng.next())
		time.sleep(r.randint(40, 100))
		print("End: " + str(int(time.time())))

	def test_find_seed(self):
		# Start: 1576284626
		# 1031238433
		# End: 1576284720
		for i in range(1576284626, 1576284720):
			prng = MersenneTwisterPRNG(i)
			if prng.next() == 1031238433:
				print("Seed was: " + str(i))




