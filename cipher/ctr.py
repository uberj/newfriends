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

	def edit(self, ciphertext: bytes, offset: int, newtext: bytes):
		return bytes(self._edit(ciphertext, offset, newtext))

	def _edit(self, ciphertext: bytes, offset: int, newtext: bytes):
		yield from ciphertext[:offset]
		yield from bytes(self._generate_edit_str(offset, newtext))
		yield from ciphertext[offset + len(newtext):]

	def _make_block(self, nonce, block_count) -> bytes:
		return self.block_cipher.encrypt(
			int.to_bytes(nonce, self.half_block_size, 'little') +
			int.to_bytes(block_count, self.half_block_size, 'little')
		)

	def _generate_key_string(self, offset) -> bytes:
		# Start emitting the keystream at the a given offset

		start_block = int(offset / self.block_size)
		offset_byte = offset % self.block_size

		cur_block = self._make_block(self.nonce, start_block)
		block_count = start_block
		i = offset_byte
		while True:
			if i >= 16:
				i = 0
				block_count += 1
				cur_block = self._make_block(self.nonce, block_count)

			yield cur_block[i]
			i += 1

	def _generate_edit_str(self, offset: int, newtext: bytes):
		e_bytes = self._generate_key_string(offset)
		for p_byte, e_byte in zip(newtext, e_bytes):
			yield p_byte ^ e_byte

