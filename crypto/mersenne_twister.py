from crypto.mersenne_twister_prng import MersenneTwisterPRNG


class MersenneTwisterCipher(object):
	def __init__(self, key: int):
		self.key = key
		self.block_size = 16
		self.half_block_size = int(self.block_size / 2)

	def _mt_next(self, plaintext: bytes) -> bytes:
		prng = MersenneTwisterPRNG(self.key)
		plaintext_blocks = [plaintext[i:i + self.block_size] for i in range(0, len(plaintext), self.block_size)]
		for block in plaintext_blocks:
			mixin_block = (
				int.to_bytes(prng.next(), 4, 'big') +
				int.to_bytes(prng.next(), 4, 'big') +
				int.to_bytes(prng.next(), 4, 'big') +
				int.to_bytes(prng.next(), 4, 'big')
			)
			for p_byte, e_byte in zip(block, mixin_block):
				yield p_byte ^ e_byte

	def encrypt(self, plaintext: bytes) -> bytes:
		return bytes(self._mt_next(plaintext))

	def decrypt(self, ciphertext: bytes) -> bytes:
		return bytes(self._mt_next(ciphertext))


