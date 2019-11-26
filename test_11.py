import unittest
import os

from Crypto.Cipher import AES
from random import choice, randint

from CBCCipher import CBCCipher
from oracle import BBoxType, oracle_guess_cipher_type
from sample_text import text as sample_text
from somecode import rand_n_string, pad16_PKCS7, xor


def random_bbox_types():
	while True:
		yield choice(list(BBoxType))


class BlackBoxBuilder(object):
	def __init__(self, order: [BBoxType] = None):
		"""
		Build a generator of crypto mystery boxes
		:param order: stack of block types that can be used for testing (when defined). 0th comes out first
		"""
		self.order = order and list(reversed(order))

	def build(self) -> (BBoxType, bytes):
		prefix = os.urandom(randint(5, 10))
		suffix = os.urandom(randint(5, 10))
		test_data = pad16_PKCS7(self.test_data())
		bbox_type = self.next_bbox_type()
		if bbox_type == BBoxType.ECB:
			cipher = AES.new(rand_n_string(16), AES.MODE_ECB)
			box_content = cipher.encrypt(test_data)
		elif bbox_type == BBoxType.CBC:
			cipher = CBCCipher(rand_n_string(16), rand_n_string(16))
			box_content = cipher.encrypt(test_data)
		else:
			raise NotImplemented("Cannot handle box type: " + str(bbox_type))

		return bbox_type, prefix + box_content + suffix

	@staticmethod
	def test_data() -> bytes:
		# Make sure there is some duplicate text for now.
		return sample_text.encode()

	def next_bbox_type(self):
		if not self.order:
			return choice(list(BBoxType))
		else:
			return self.order.pop()


class TestChallenge11(unittest.TestCase):
	def test_ecb_detect(self):
		bbbuilder = BlackBoxBuilder(order=[BBoxType.ECB])
		bbtype, mystery_text = bbbuilder.build()
		guess = oracle_guess_cipher_type(mystery_text)
		self.assertEqual(guess, BBoxType.ECB)

	def test_cbc_detect(self):
		bbbuilder = BlackBoxBuilder(order=[BBoxType.CBC])
		bbtype, mystery_text = bbbuilder.build()
		guess = oracle_guess_cipher_type(mystery_text)
		self.assertEqual(guess, BBoxType.CBC)

	def test_cbc_random(self):
		bbbuilder = BlackBoxBuilder()
		for _ in range(100):
			bbtype, mystery_text = bbbuilder.build()
			guess = oracle_guess_cipher_type(mystery_text)
			self.assertEqual(guess, bbtype)

