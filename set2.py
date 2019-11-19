from set1 import pad_PKCS7, xor


class CBCCipher(object):
	def __init__(self, key: str, iv: str):
		self.key = pad_PKCS7(key.encode())
		self.iv = pad_PKCS7(iv.encode())

	def encrypt(self, b: str) -> bytes:
		"""
		:param b: message to be encrypted
		:return: encrypted byte string
		"""
		bs = b.encode()
		last = self.iv
		encrypted_chunks = []  # Encrypted chunks
		for i in range(0, len(pad_PKCS7(bs)), 16):
			plaintext_block = bs[i:i + 16]
			e_chunk = xor(self.key, xor(last, plaintext_block))
			encrypted_chunks.append(e_chunk)
			last = e_chunk

		return b''.join(encrypted_chunks)

	def decrypt(self, bs: bytes) -> str:
		last = self.iv
		encrypted_chunks = []  # Encrypted chunks
		for i in range(0, len(pad_PKCS7(bs)), 16):
			ciphertext_block = bs[i:i + 16]
			de_chunk = xor(self.key, xor(last, ciphertext_block))
			encrypted_chunks.append(de_chunk)
			last = ciphertext_block

		return b''.join(encrypted_chunks).decode()


