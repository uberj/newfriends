import unittest
from random import choice
from binascii import a2b_base64

from crypto.cbc import CBCCipher
from util.somecode import pad16_PKCS7, unpad16_PKCS7, rand_n_string, PaddingException

FIXED_KEY = rand_n_string(16).encode()
FIXED_IV = rand_n_string(16).encode()

PSTRINGS = [
	b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
	b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
	b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
	b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
	b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
	b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
	b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
	b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
	b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
	b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
]
FIXED_STRING = a2b_base64(choice(PSTRINGS))

PText = int  # Plaintext byte
Mi = int  # The modifier byte that causes a valid pad for the ith byte


def cipher_text_provider() -> (bytes, bytes):
	p = pad16_PKCS7(FIXED_STRING)
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	return FIXED_IV, cipher.encrypt(p)


def padding_oracle(cipher_text) -> bool:
	cipher = CBCCipher(FIXED_KEY, FIXED_IV)
	decrypt = cipher.decrypt(cipher_text)
	try:
		unpad16_PKCS7(decrypt)
	except PaddingException:
		return False
	return True


def build_pad(a: bytes, suffix: [(PText, Mi)], pad_value: int):
	pad = b''
	for (p, mi) in suffix:
		pad += bytes([pad_value ^ mi])

	return pad


def attack_byte(cipher_blocks: [bytes], a: [bytes], b: [bytes], bidx: int, plain_text_suffix: [(PText, Mi)])\
		-> [(PText, Mi)]:
	"""
	@param cipher_blocks: These are the blocks not involved in the attack, but must be passed to the oracle
	@param a: This is the block prior to cipher_block1. We manipulate this block to indirectly manipulate cipher_block1
	@param b: This is the block after to cipher_block0. We are attacking this block
	@param bidx: The index of the byte we are attacking (in cipher_block1)
	"""
	pad_length = 15 - bidx

	# We have to know what the plain_text is to construct a proper pad of pad_length
	if len(plain_text_suffix) != pad_length:
		assert len(plain_text_suffix) == pad_length

	# Store the byte we are going to attack. We'll need this later
	a_i = a[bidx]

	pad_modifier = build_pad(a, plain_text_suffix, pad_length + 1)

	oracle_guesses = []
	for c_m in range(256):

		# Construct the attack
		attack_block = a[0:bidx] + bytes([c_m]) + pad_modifier

		# use oracle
		attack_str = b''.join(cipher_blocks + [attack_block, b])
		if padding_oracle(attack_str):
			oracle_guesses.append(c_m)

	if not oracle_guesses:
		raise Exception("We didn't find our attack vector")

	# Start trying bytes until our oracle says we have correct padding
	possible_solutions = []
	for c_m in oracle_guesses:
		# calculate what the plain text byte was
		# Use:
		#  * What we know the padding has to be -> pad_length + 1
		#  * What byte caused that correct padding  -> c_m
		#  * What the original cipher_text byte was -> c_0
		#  * What the original decrypted text was -> d_k
		t = pad_length + 1
		d_k = t ^ c_m
		p = d_k ^ a_i
		possible_solutions.append((p, d_k))
	return possible_solutions


def padding_oracle_attack(iv, cipher_text):
	plain_text: bytes = b''
	cipher_blocks: [bytes] = [cipher_text[i:i + 16] for i in range(0, len(cipher_text), 16)]
	cipher_blocks.insert(0, iv)
	for cur_block_idx in reversed(range(1, len(cipher_blocks))):
		prev_solutions: [(PText, Mi)] = []
		prev_blocks: [bytes] = cipher_blocks[:cur_block_idx - 1]
		cipher_block0: [bytes] = cipher_blocks[cur_block_idx - 1]
		cipher_block1: [bytes] = cipher_blocks[cur_block_idx]
		for idx_byte_offset in range(16):
			byte_attack_idx: int = 15 - idx_byte_offset
			possible_solutions: (PText, Mi) = attack_byte(
				prev_blocks, cipher_block0, cipher_block1, byte_attack_idx, prev_solutions)

			found_solution = False
			# A recursive search really would have been more elligant here.
			# I find that every so often a failure happens with the tests
			# I think its because I need to explore further than 1 byte with each possible solution
			for solution in possible_solutions:
				try:
					# The last byte doesn't need to check options
					if byte_attack_idx != 0:
						# If its not the last byte, then
						# The byte is valid depending on whether it helps solve the next byte
						attack_byte(prev_blocks, cipher_block0, cipher_block1, byte_attack_idx - 1, [solution] + prev_solutions)

					found_solution = solution
					break
				except Exception:
					continue

			if not found_solution:
				raise Exception("No solution")

			prev_solutions.insert(0, found_solution)
			plain_text = chr(found_solution[0]).encode() + plain_text
	return plain_text


class TestChallenge17(unittest.TestCase):
	def test_select_string(self):
		iv, cipher_text = cipher_text_provider()
		self.assertIsNotNone(iv)
		self.assertIsNotNone(cipher_text)

	def test_consumer(self):
		iv, cipher_text = cipher_text_provider()

		pad_test0 = padding_oracle(cipher_text)
		self.assertTrue(pad_test0)

		pad_test1 = padding_oracle(cipher_text[2:] + b"\xff" + b"\xff")
		self.assertFalse(pad_test1)

	def test_attack(self):
		iv, cipher_text = cipher_text_provider()
		plain_text = padding_oracle_attack(iv, cipher_text)
		text = unpad16_PKCS7(plain_text)
		self.assertEquals(FIXED_STRING, text)
