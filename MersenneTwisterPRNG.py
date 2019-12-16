class MersenneTwisterPRNG(object):
	def __init__(self, seed, mode="32"):
		self.seed = seed
		if mode == "32":
			(self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
			self.a = int("9908B0DF16", 16)
			(self.u, self.d) = (11, int("FFFFFFFF", 16))  # right shift
			(self.s, self.b) = (7, int("9D2C5680", 16))  # Left shift
			(self.t, self.c) = (15, int("EFC60000", 16))  # Left shift
			self.l = 18
			self.f = 1812433253
		elif mode == "64":
			(self.w, self.n, self.m, self.r) = (64, 312, 156, 31)
			self.a = int("B5026F5AA96619E916", 16)
			(self.u, self.d) = (29, int("5555555555555555", 16))
			(self.s, self.b) = (17, int("71D67FFFEDA60000", 16))
			(self.t, self.c) = (37, int("FFF7EEE000000000", 16))
			self.l = 43
			self.f = 6364136223846793005
		else:
			raise RuntimeError("No mode: " + mode)

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
		y = y ^ ((y >> self.u) & self.d)
		# y := y xor ((y << s) and b)
		y = y ^ ((y << self.s) & self.b)
		# y := y xor ((y << t) and c)
		y = y ^ ((y << self.t) & self.c)
		# y := y xor (y >> l)
		y = y ^ (y >> self.l)
		return y

	@classmethod
	def top_bom_masks(self, l) -> (int, int, int):
		return (
			int((32 - (2 * l)) * "1" + l * "0" + l * "0", 2),
			int((32 - (2 * l)) * "0" + l * "1" + l * "0", 2),
			int((32 - (2 * l)) * "0" + l * "0" + l * "1", 2),
		)

	def invert_left_shift(self, y_p:int, l:int, u:int) -> int:
		"""
		y_p: y prime.
		l: left shift value. call
		u: the bit wise "and" constant
		# TODO, link to the notes page
		"""
		top_a_mask, top_b_mask, bot_y_mask = self.top_bom_masks(l)
		top_a_y_p, top_b_y_p, bot_y_p = (
			y_p & top_a_mask,
			y_p & top_b_mask,
			y_p & bot_y_mask
		)
		print("top_a_y_p: " + bin(top_a_y_p))
		print("top_b_y_p: ", bin(top_b_y_p))
		print("bot_y_p: ", bin(bot_y_p))
		return None

	def invert_temper(self, y):
		"""
		u = 11
		s = 7
		t = 15
		:param y:
		:return:
		"""
		# y = y ^ (y >> self.l)
		# Top is the y shifted l (18) bits. This is the highest 14 bits
		top14 = y >> self.l
		bottom_mask = 2 ** (32 - self.l) - 1
		bottom18 = y & bottom_mask
		y = (top14 << self.l) + (top14 ^ bottom18)

		# y = y ^ ((y << self.t) & self.c)

		# y = y ^ ((y >> self.u) & self.d)

		# y = y ^ ((y << self.s) & self.b)
		return y & (2 ** self.w - 1)




