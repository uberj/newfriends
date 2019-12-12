from somecode import pad16_PKCS7, xor
from Crypto.Cipher import AES


class CTRCipher(object):
	def __init__(self, key: bytes, nonce: int):
		self.key = key
		self.nonce = nonce
		self.block_cipher = AES.new(self.key, AES.MODE_ECB)
		self.block_size = 16
		self.half_block_size = int(self.block_size / 2)

	def _ctr(self, plaintext: bytes) -> bytes:
		plaintext_blocks = [plaintext[i:i + self.block_size] for i in range(0, len(plaintext), self.block_size)]
		for i, block in enumerate(plaintext_blocks):
			mixin_block = self.block_cipher.encrypt(
				int.to_bytes(self.nonce, self.half_block_size, 'little') +
				int.to_bytes(i, self.half_block_size, 'little')
			)
			for p_byte, e_byte in zip(block, mixin_block):
				yield p_byte ^ e_byte

	def encrypt(self, plaintext: bytes) -> bytes:
		return bytes(self._ctr(plaintext))

	def decrypt(self, ciphertext: bytes) -> bytes:
		return bytes(self._ctr(ciphertext))


