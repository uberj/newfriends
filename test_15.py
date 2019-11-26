import unittest
import string
from set1 import pad16_PKCS7


def unpad16_PKCS7(padded: bytes) -> bytes:
	expected_pad_count = padded[-1]
	if chr(expected_pad_count) in string.printable:
		if len(padded) % 16:
			raise Exception("Bad padding")
		else:
			return padded

	expected_pad = (chr(expected_pad_count) * expected_pad_count).encode()
	if not padded.endswith(expected_pad):
		raise Exception("Bad padding")

	return padded.rstrip(expected_pad)


class TestChallenge15(unittest.TestCase):
	def test_detect_good_pad(self):
		self.assertEquals(unpad16_PKCS7(b"ICE ICE BABY\x04\x04\x04\x04"), b"ICE ICE BABY")
		self.assertEquals(unpad16_PKCS7(b"YELLOW SUBMARINE"), b"YELLOW SUBMARINE")

	def test_detect_bad_pad(self):
		self.assertRaises(Exception, unpad16_PKCS7, b"ICE ICE BABY\x05\x05\x05\x05")
		self.assertRaises(Exception, unpad16_PKCS7, b"ICE ICE BABY\x01\x02\x03\x04")
		self.assertRaises(Exception, unpad16_PKCS7, b"ICE IABY\x01\x02X")
