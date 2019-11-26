import unittest

from Crypto.Cipher import AES

from CBCCipher import CBCCipher
from somecode import pad16_PKCS7, unpad16_PKCS7, rand_n_string

FIXED_KEY = rand_n_string(16).encode()
FIXED_IV = rand_n_string(16).encode()


def encrypt_data(user_data: bytes) -> bytes:
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	s = b"comment1=cooking%20MCs;userdata=" \
		+ user_data.replace(b";", b"").replace(b"=", b"") \
		+ b";comment2=%20like%20a%20pound%20of%20bacon"

	pkcs_ = pad16_PKCS7(s)
	return cipher.encrypt(pkcs_)


def check_admin(blob: bytes) -> bool:
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	decrypt = cipher.decrypt(blob)
	return b";admin=true;" in decrypt


class TestChallenge16(unittest.TestCase):
	def test_plain(self):
		cipher_text = encrypt_data(b"XXXXXX")
		admin_check = check_admin(cipher_text)
		self.assertFalse(admin_check)
