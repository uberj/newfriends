from set1 import pad_PKCS7, xor
from Crypto.Cipher import AES


class CBCCipher(object):
	def __init__(self, key: str, iv: str):
		self.key = pad_PKCS7(key.encode())
		self.iv = pad_PKCS7(iv.encode())
		self.cipher = AES.new(self.key, AES.MODE_ECB)

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
			e_chunk = self.cipher.encrypt(xor(last, plaintext_block))
			encrypted_chunks.append(e_chunk)
			last = e_chunk

		return b''.join(encrypted_chunks)

	def decrypt(self, bs: bytes) -> bytes:
		decrypted_chunks = []  # Encrypted chunks
		last = self.iv
		for i in range(0, len(pad_PKCS7(bs)), 16):
			ciphertext_block = bs[i:i + 16]
			plain_chunk = xor(last, self.cipher.decrypt(ciphertext_block))
			decrypted_chunks.append(plain_chunk)
			last = ciphertext_block

		return b''.join(decrypted_chunks)


