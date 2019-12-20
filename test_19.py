import unittest
from cipher.ctr_cipher import CTRCipher
from binascii import a2b_base64

from util.bettercode import transpose, frequency_analysis_score
from util.somecode import rand_n_string

CHALLENGE_19_DATA = list(map(a2b_base64, [
	b'SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==',
	b'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=',
	b'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==',
	b'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=',
	b'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk',
	b'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
	b'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=',
	b'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
	b'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=',
	b'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl',
	b'VG8gcGxlYXNlIGEgY29tcGFuaW9u',
	b'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==',
	b'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=',
	b'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==',
	b'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=',
	b'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
	b'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==',
	b'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==',
	b'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==',
	b'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==',
	b'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==',
	b'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==',
	b'U2hlIHJvZGUgdG8gaGFycmllcnM/',
	b'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=',
	b'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=',
	b'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=',
	b'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=',
	b'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==',
	b'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==',
	b'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=',
	b'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==',
	b'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu',
	b'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=',
	b'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs',
	b'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=',
	b'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0',
	b'SW4gdGhlIGNhc3VhbCBjb21lZHk7',
	b'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=',
	b'VHJhbnNmb3JtZWQgdXR0ZXJseTo=',
	b'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
]))


def get_challenge_20_data():
	with open("20.txt", "r") as fd:
		for line in fd.readlines():
			yield a2b_base64(line.strip().encode())


def challenge_encrypt(p_strings):
	fixed_key = rand_n_string(16).encode()
	e_strings = []
	for plain in p_strings:
		ctr = CTRCipher(fixed_key, 0)
		e_strings.append(ctr.encrypt(plain))
	return e_strings


def simplify_structure(cipher_texts: [bytes]) -> [bytes]:
	"""
	Take variable length byte arrays and convert them all to n-byte arrays where n is the smallest variable array
	"""
	simplified = []
	shortest_block = min(map(len, cipher_texts))
	# create same size matrix
	for ct in cipher_texts:
		simplified.append(ct[0:shortest_block])
	return simplified


def freq_analysis(cipher_text: bytes) -> int:
	best = None
	for c in range(256):
		candidate = apply_decrypt_byte(c, cipher_text)
		score = frequency_analysis_score(candidate)
		if not best or score > best[0]:
			best = (score, c, candidate)

	return best[1]


def apply_decrypt_byte(decrypt_byte: int, cipher_text: bytes) -> bytes:
	decrypted = []
	for b in cipher_text:
		decrypted.append(b ^ decrypt_byte)
	return bytes(decrypted)

def attack(to_attack):
	e_strings = challenge_encrypt(to_attack)
	cipher_texts = simplify_structure(e_strings)
	ith_blocks: [bytes] = transpose(cipher_texts)

	# figure out the most likely decrypt byte using fre-analysis
	# decrypt using that byte
	decrypted_blocks: [bytes] = []
	for blocks in ith_blocks:
		best_decrypt_byte = freq_analysis(blocks)
		decrypted_block = apply_decrypt_byte(best_decrypt_byte, blocks)
		decrypted_blocks.append(decrypted_block)

	# transpose again to get plain text blocks
	return transpose(decrypted_blocks)


class TestChallenge19And20(unittest.TestCase):
	def test_transpose(self):
		t = transpose([b'\x01\x02\x03', b'\x01\x02\x03', b'\x01\x02\x03', b'\x01\x02\x03'])
		self.assertEquals(t[0], b'\x01' * 4)
		self.assertEquals(t[1], b'\x02' * 4)
		self.assertEquals(t[2], b'\x03' * 4)

	def test_challenge_19(self):
		self.assertTrue(b'he, too, has resigne' in attack(CHALLENGE_19_DATA))

	def test_challenge_20(self):
		# Turns out I did 19 the way 20 was supposed to go
		self.assertTrue(attack(get_challenge_20_data())[1].startswith(b'cuz I came back'))

