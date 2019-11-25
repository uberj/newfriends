import unittest
from Crypto.Cipher import AES

from set1 import rand_n_string, pad_PKCS7
FIXED_KEY = "YELLOW SUBMARINE"
cipher = AES.new(FIXED_KEY, AES.MODE_ECB)


def encrypt(plain_text: bytes) -> bytes:
	return cipher.encrypt(pad_PKCS7(plain_text))


def decrypt(cipher_text: bytes) -> bytes:
	return cipher.decrypt(cipher_text)


def decrypt_parse(cipher_text: bytes) -> dict:
	decrypt = cipher.decrypt(cipher_text)
	return bytes_to_dict(decrypt)


def bytes_to_dict(s: bytes) -> dict:
	kvs = s.decode().split("&")
	d = {}
	for k, v in [kv.split("=") for kv in kvs]:
		if v.isdigit():
			d[k] = int(v)
		else:
			d[k] = v
	return d


def dict_to_str(d: dict) -> bytes:
	s = ""
	for k, v in d.items():
		s += k + "=" + str(v) + "&"

	return s.rstrip("&").encode()


def profile_for(username):
	return dict_to_str({
		"email": username.replace("&", "").replace("=", ""),
		"uid": 10,
		"role": "user"
	})


class TestChallenge13(unittest.TestCase):
	def test_generate_attack(self):
		"""
		Aiming for:
			email=user@admin&uid=10&role=admin
		From the oracle, I can get:
			email=user@admin&uid=10&role=user
		Assuming 128bit blocks (16 bytes)
			email=user@admin
			&uid=10&role=use
			r
		If I pad the username a bit I can get
			"1234567890123456"
			"email=userXXX@ad"
			"min&uid=10&role="
			"user            "
		Then, we can use the oracle to 

		:return:
		"""

	def test_structured_string(self):
		x = {"a": 1, "b": "c"}
		d = dict_to_str(x)
		to_dict = bytes_to_dict(d)
		self.assertEqual(x, to_dict)

	def test_profile_for(self):
		self.assertEqual("email=user@admin&uid=10&role=user", profile_for("user@admin"))

	def test_profile_for_sanitize(self):
		self.assertEqual("email=user@admin&uid=10&role=user", profile_for("use&r@adm=in"))
