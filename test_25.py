import unittest

from util.somecode import rand_n_string
from cipher.ctr import CTRCipher
from binascii import a2b_base64
import string
import random

R = random.Random()
FIXED_KEY = rand_n_string(16).encode()


def challenge_input() -> bytes:
	with open("challenge_inputs/25.txt", "r") as fd:
		return a2b_base64(fd.read())



def moving_windows(block_size, end) -> ((int, int), (int, int)):
	"""
	A window is ((a, b), (c, d))
	a, c = index where edit starts
	b, d = index where edit ends

	 a   bXc        d
	|----------------|
	The byte between b and c (X) is what will *not* have an edit

	"""
	for block_offset in range(0, end, block_size):
		start_offset = block_offset * block_size
		for byte_offset in range(16):
			start = (start_offset, start_offset + byte_offset)
			end = (start_offset + byte_offset + 1, start_offset + block_size)
			yield start, end


class TestChallenge25(unittest.TestCase):
	def test_sliding_window(self):
		windows = list(moving_windows(16, 16))
		self.assertEqual(16, len(windows))
		self.assertEqual(((0, 0), (1, 16)), windows[0])
		self.assertEqual(((0, 1), (2, 16)), windows[1])
		self.assertEqual(((0, 2), (3, 16)), windows[2])
		self.assertEqual(((0, 3), (4, 16)), windows[3])
		self.assertEqual(((0, 4), (5, 16)), windows[4])
		self.assertEqual(((0, 5), (6, 16)), windows[5])
		self.assertEqual(((0, 6), (7, 16)), windows[6])
		self.assertEqual(((0, 7), (8, 16)), windows[7])
		self.assertEqual(((0, 8), (9, 16)), windows[8])
		self.assertEqual(((0, 9), (10, 16)), windows[9])
		self.assertEqual(((0, 10), (11, 16)), windows[10])
		self.assertEqual(((0, 11), (12, 16)), windows[11])
		self.assertEqual(((0, 12), (13, 16)), windows[12])
		self.assertEqual(((0, 13), (14, 16)), windows[13])
		self.assertEqual(((0, 14), (15, 16)), windows[14])
		self.assertEqual(((0, 15), (16, 16)), windows[15])

	def test_attack_challenge_input(self):
		"""
		This attack is going to work a lot like the CBC attack.
		We will surround a byte with know bytes (we'll store this block value)
			* We'll compute offsets to use with our edit() call
			* The offset pair are called a "window"
		We'll compute all the possible ciphertexts of the byte we surrounded
		Then compare to our stored value
		"""
		to_attack = challenge_input()
		for window in moving_windows():
			print(window)

	def test_edit(self):
		cipher = CTRCipher(key=FIXED_KEY, nonce=0)
		n_string = rand_n_string(10000).encode()
		orig = cipher.encrypt(n_string)

		# The string we are going to inject
		edit_string = string.ascii_lowercase.encode()[:16]

		# Test 20 random edits
		for i in range(20):
			offset = R.randint(0, 1000)
			# make sure its not already there (very unlikely, but lets make sure)
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
