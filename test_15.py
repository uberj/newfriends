import unittest
from util.somecode import unpad16_PKCS7, PaddingException, pad16_PKCS7


class TestChallenge15(unittest.TestCase):
	def test_pad_0(self):
		pkcs_ = pad16_PKCS7(b"YELLOW SUBMARINE")
		self.assertEqual(pkcs_, b"YELLOW SUBMARINE\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10")

	def test_pad_1(self):
		pkcs_ = pad16_PKCS7(b"ICE ICE BABY")
		self.assertEqual(pkcs_, b"ICE ICE BABY\x04\x04\x04\x04")

	def test_detect_good_pad(self):
		self.assertEqual(unpad16_PKCS7(b"ICE ICE BABY\x04\x04\x04\x04"), b"ICE ICE BABY")
		self.assertEqual(unpad16_PKCS7(b"YELLOW SUBMARINE\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"), b"YELLOW SUBMARINE")

	def test_detect_bad_pad(self):
		self.assertRaises(PaddingException, unpad16_PKCS7, b"_\x8a\x95\xbeh\xac\xec\x96\xde+u\x16\xe0u\x9e\xf5\xb7\xc1\x0b9\xc9\xf8\xf0\xeas\xcf\xfa\xa5\xb6\xea\xd3\x13\xbdHc\x88\x0f\x10\xfbj\xdf\xa5\x1eHYM\xec\xae\x0cH\x9e\xc3H\x8c\x1a\x9f\x93r\x9aK\x8f\x07\x8eu")
		self.assertRaises(PaddingException, unpad16_PKCS7, b"ICE ICE BABY\x05\x05\x05\x05")
		self.assertRaises(PaddingException, unpad16_PKCS7, b"ICE ICE BABY\x01\x02\x03\x04")
		self.assertRaises(PaddingException, unpad16_PKCS7, b"ICE IABY\x01\x02X")
