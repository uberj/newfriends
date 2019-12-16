import math

class MersenneTwisterPRNG(object):
	def __init__(self, seed):
		self.seed = seed
		(self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
		self.a = int("9908B0DF16", 16)
		(self.u, self.d) = (11, int("FFFFFFFF", 16))  # right shift
		(self.s, self.b) = (7, int("9D2C5680", 16))  # Left shift
		(self.t, self.c) = (15, int("EFC60000", 16))  # Left shift
		self.l = 18
		self.f = 1812433253

		# // Create a length n array to store the state of the generator
		# int[0..n-1] MT
		self.mT = [0] * self.n
		# int index := n+1
		self.index = self.n + 1
		# const int lower_mask = (1 << r) - 1 // That is, the binary number of r 1's
		self.lower_mask = (1 << self.r) - 1
		# const int upper_mask = lowest w bits of (not lower_mask)
		self.upper_mask = ((1 << self.r) - 1) << (self.r + 1)
		self._seed()

	def _seed(self):
		# // Initialize the generator from a seed
		# index := n
		self.index = self.n
		# MT[0] := seed
		self.mT[0] = self.seed
		for i in range(1, len(self.mT)): # // loop over each element
			# MT[i] := lowest w bits of (f * (MT[i-1] xor (MT[i-1] >> (w-2))) + i)
			self.mT[i] = (2 ** self.w - 1) & (self.f * (self.mT[i - 1] ^ (self.mT[i - 1] >> (self.w - 2))) + 1)

	def _twist(self):
		# // Generate the next n values from the series x_i
		# for i from 0 to (n-1) {
		for i in range(self.n):
			# int x := (MT[i] and upper_mask) + (MT[(i+1) mod n] and lower_mask)
			x = (self.mT[i] & self.upper_mask) + (self.mT[(i + 1) % self.n] & self.lower_mask)
			# int xA := x >> 1
			xA = x >> 1
			# if (x mod 2) != 0 { // lowest bit of x is 1
			if x % 2 != 0:
				# xA := xA xor a
				xA = xA ^ self.a
			# }
			# MT[i] := MT[(i + m) mod n] xor xA
			self.mT[i] = self.mT[(i + self.m) % self.n] ^ xA
		# }
		# index := 0
		self.index = 0

	def next(self):
		# // Extract a tempered value based on MT[index]
		# // calling twist() every n numbers
		# if index >= n {
		# if index > n {
		# error "Generator was never seeded"
		# // Alternatively, seed with constant value; 5489 is used in reference C code[48]
		# }
		# twist()
		# }
		if self.index >= self.n:
			if self.index > self.n:
				raise Exception("No seed?")
			self._twist()

		# int y := MT[index]
		y = self.mT[self.index]
		y = self.temper(y)

		# index := index + 1
		self.index += 1
		# return lowest w bits of (y)
		return (2 ** self.w - 1) & y

	def temper(self, y):
		# y := y xor ((y >> u) and d)
		# y := y xor ((y << s) and b)
		# y := y xor ((y << t) and c)
		# y := y xor (y >> l)
		y = y ^ ((y >> self.u) & self.d)
		y = y ^ ((y << self.s) & self.b)
		y = y ^ ((y << self.t) & self.c)
		y = y ^ (y >> self.l)
		return y

	def invert_temper(self, y_p):
		y_p = self.invert_right_shift(y_p, self.l, 2**self.w - 1)
		y_p = self.invert_left_shift(y_p, self.t, self.c)
		y_p = self.invert_left_shift(y_p, self.s, self.b)
		y = self.invert_right_shift(y_p, self.u, self.d)
		return y

	@classmethod
	def bit_slice(self, x: int, i: int, l: int):
		t = "1" * l + "0" * (l * i)
		return (x & int(t, 2) ) >> (l * i)

	@classmethod
	def invert_left_shift(self, y_p:int, l:int, u:int) -> int:
		"""
		y_p: y prime.
		l: left shift value. call
		u: the bit wise "and" constant
		# TODO, link to the notes page
		"""
		y = 0
		prev_t = 0
		for i in range(0, math.ceil(32/l)):
			# i is the starting point for this round
			# t is the temp variable for this steps result
			y_p_slice = self.bit_slice(y_p, i, l)
			u_slice = self.bit_slice(u, i, l)
			t = y_p_slice ^ (prev_t & u_slice)
			y += (t << (i * l))
			prev_t = t

		return y & (2**32 - 1)

	@classmethod
	def bin_rev(cls, x):
		return int("".join(reversed(bin(x)[2:].rjust(32, "0"))), 2)

	@classmethod
	def invert_right_shift(cls, y_p, l, u):
		y_p, u = (cls.bin_rev(y_p), cls.bin_rev(u))
		lshift = cls.invert_left_shift(y_p, l, u)
		return cls.bin_rev(lshift)




