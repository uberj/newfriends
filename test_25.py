import unittest

from util.somecode import rand_n_string
from cipher.ctr import CTRCipher
from binascii import a2b_base64
import string

FIXED_KEY = rand_n_string(16).encode()


def challenge_input() -> bytes:
	with open("challenge_inputs/25.txt", "r") as fd:
		return a2b_base64(fd.read())


class TestChallenge25(unittest.TestCase):
	def test_edit(self):
		cipher = CTRCipher(key=FIXED_KEY, nonce=0)
		n_string = ("A" * 100).encode()
		orig = cipher.encrypt(n_string)

		# The string we are going to inject
		edit_string = string.ascii_lowercase.encode()[:16]

		# make sure its not already there (very unlikely, but lets make sure)
		offset = 1
		self.assertNotEqual(orig[offset:len(edit_string)], edit_string)

		# make the edit
		edit = cipher.edit(orig, offset, edit_string)

		# decrypt the edit to see if it worked
		modified = cipher.decrypt(edit)

		# The length should be the same, this was an insert
		self.assertEqual(len(n_string), len(modified))

		# Did the edit make it in?
		self.assertEqual(modified[offset:len(edit_string) + offset], edit_string)

		# Is the ciphertext prefix the same?
		self.assertEqual(edit[:offset], orig[:offset])
		# Is the plaintext prefix the same?
		self.assertEqual(modified[:offset], n_string[:offset])

		# Is ciphertext suffix the same?
		self.assertEqual(edit[offset + len(edit_string):], orig[offset + len(edit_string):])
		# Is the plaintext suffix the same?
		self.assertEqual(n_string[offset + len(edit_string):], modified[offset + len(edit_string):])
