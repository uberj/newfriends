import unittest

from cipher.cbc_cipher import CBCCipher
from util.somecode import pad16_PKCS7, unpad16_PKCS7, rand_n_string

FIXED_KEY = rand_n_string(16).encode()
FIXED_IV = rand_n_string(16).encode()


def encrypt_data(user_data: bytes) -> bytes:
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	s = b"comment1=cooking%20MCs;userdata=" \
		+ user_data.replace(b";", b"").replace(b"=", b"") \
		+ b";comment2=%20like%20a%20pound%20of%20bacon"

	return cipher.encrypt(pad16_PKCS7(s))


def check_admin(blob: bytes) -> bool:
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	decrypt = cipher.decrypt(blob)
	return b";admin=true;" in unpad16_PKCS7(decrypt)


class TestChallenge16(unittest.TestCase):
	def test_plain(self):
		cipher_text = encrypt_data(b"XXXXXX")
		admin_check = check_admin(cipher_text)
		self.assertFalse(admin_check)

	def test_attack(self):
		"""
		Here are the blocks!

		comment1=cooking
		%20MCs;userdata=
		(User here)
		;comment2=%20lik
		e%20a%20pound%20
		of%20bacon

		I want something like:

		%20MCs;userdata=
		YYYYYYYYYYYYYYYY
		;admin=true;XXXX
		;comment2=%20lik

		ord(":") -> 58
		bin(58) -> 0b111010
		--- change 1 bit ---
		0b111010 ^ 0b000001 -> 0b111011
		0b111011 -> 59
		chr(59) -> ";"

		Simplified and expanded to the other character:
		chr(ord(':') ^ 0b000001) -> ';'
		chr(ord('=') ^ 0b000001) -> '<'

		Following rules I can get:

		0123456789012345
		YYYYYYYYYYYYYYYY
		:admin>true:XXXX

		I encrypt...
		I take my encrypted "YY.." block...
		I change the 0th, 6th, and 11th  byte to "0b000001"

		I check admin on that.
		Let us see if that works!
		(Will try later)

		:return:
		"""
		pass
