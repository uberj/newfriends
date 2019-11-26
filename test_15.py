import unittest
from somecode import unpad16_PKCS7


class TestChallenge15(unittest.TestCase):
	def test_detect_good_pad(self):
		self.assertEquals(unpad16_PKCS7(b"ICE ICE BABY\x04\x04\x04\x04"), b"ICE ICE BABY")
		self.assertEquals(unpad16_PKCS7(b"YELLOW SUBMARINE"), b"YELLOW SUBMARINE")

	def test_detect_bad_pad(self):
		self.assertRaises(Exception, unpad16_PKCS7, b"ICE ICE BABY\x05\x05\x05\x05")
		self.assertRaises(Exception, unpad16_PKCS7, b"ICE ICE BABY\x01\x02\x03\x04")
		self.assertRaises(Exception, unpad16_PKCS7, b"ICE IABY\x01\x02X")
