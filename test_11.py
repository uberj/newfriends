import unittest
import os

from enum import Enum
from Crypto.Cipher import AES
from random import choice, randint

from CBCCipher import CBCCipher
from sample_text import text as sample_text
from set1 import rand_n_string, pad_PKCS7
from ecb_util import ordered_block_counts


class BBoxType(Enum):
	ECB = "ECB"
	CBC = "CBC"
	RANDOM = "RANDOM"


def random_bbox_types():
	while True:
		yield choice(list(BBoxType))


class BlackBoxBuilder(object):
	def __init__(self, order: [BBoxType] = None):
		"""
		Build a generator of crypto mystery boxes
		:param order: stack of block types that can be used for testing (when defined). 0th comes out first
		"""
		self.order = list(reversed(order))

	def build(self) -> (BBoxType, bytes):
		prefix = os.urandom(randint(5, 10))
		suffix = os.urandom(randint(5, 10))
		test_data = pad_PKCS7(self.test_data())
		bbox_type = self.next_bbox_type()
		if bbox_type == BBoxType.ECB:
			cipher = AES.new(rand_n_string(16), AES.MODE_ECB)
			box_content = cipher.encrypt(test_data)
		elif bbox_type == BBoxType.CBC:
			cipher = CBCCipher(rand_n_string(16), rand_n_string(16))
			box_content = cipher.encrypt(test_data)
		elif bbox_type == BBoxType.RANDOM:
			box_content = os.urandom(len(test_data))
		else:
			raise NotImplemented("Cannot handle box type: " + str(bbox_type))

		return bbox_type, prefix + box_content + suffix

	@staticmethod
	def test_data() -> bytes:
		# Make sure there is some duplicate text for now.
		return (sample_text + "a" * 25 + sample_text).encode()

	def next_bbox_type(self):
		if not self.order:
			return choice(list(BBoxType))
		else:
			return self.order.pop()



class TestChallenge11(unittest.TestCase):
	def test_ecb_detect(self):
		bbbuilder = BlackBoxBuilder()
		mystery_text = bbbuilder.build()
		print(ordered_block_counts(mystery_text))
