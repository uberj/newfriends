import unittest
from Crypto.Cipher import AES

from util.somecode import pad16_PKCS7
FIXED_KEY = "YELLOW SUBMARINE"
cipher = AES.new(FIXED_KEY, AES.MODE_ECB)


def encrypt(plain_text: bytes) -> bytes:
	return cipher.encrypt(pad16_PKCS7(plain_text))


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
		If I pad the username a bit I can get (call this paste_target)
			"email=userXXX@ad" (0:15)
			"min&uid=10&role=" (16:31)
			"user            " (32:47)
		Then, we can use the oracle to create an identity like: (call this copy_target)
			"email=userXXXXX@" (0:15)
			"admin           " (16:31) <-- now we reuse this block (copy-and-paste)
			"&uid=10&role=use" (32:47)
			"r               " (48:64)
		"""
		paste_target = encrypt(profile_for("userXXX@admin"))
		self.assertTrue(len(paste_target), 48)

		copy_target = encrypt(profile_for("userXXXXX@admin           "))
		self.assertTrue(len(copy_target), 64)

		fake_profile_bytes = paste_target[0:32] + copy_target[16:32]

		fake_profile_encoded = decrypt(fake_profile_bytes)
		fake_profile = bytes_to_dict(fake_profile_encoded)
		self.assertEqual(fake_profile["role"].strip(), "admin")

	def test_structured_string(self):
		x = {"a": 1, "b": "c"}
		d = dict_to_str(x)
		to_dict = bytes_to_dict(d)
		self.assertEqual(x, to_dict)

	def test_profile_for(self):
		self.assertEqual(b"email=user@admin&uid=10&role=user", profile_for("user@admin"))

	def test_profile_for_sanitize(self):
		self.assertEqual(b"email=user@admin&uid=10&role=user", profile_for("use&r@adm=in"))
