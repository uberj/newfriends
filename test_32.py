import unittest
import time
import requests
import random
import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qsl

from http import HTTPStatus
from multiprocessing import Process

from crypto.hmac import hmac_sha1
from util.bettercode import random_word

HOST = '127.0.0.1'
PORT = random.randint(7000, 9000)
URL = "http://" + HOST + ":" + str(PORT)

SECRET = random_word()
ARTIFICIAL_DELAY = 0.005


def insecure_compare(hmac: bytes, signature: bytes):
	if len(hmac) != len(signature):
		return False

	for a, b in zip(hmac, signature):
		if a != b:
			return False
		time.sleep(ARTIFICIAL_DELAY)

	return True


class RequestHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		parsed = urlparse(self.path)
		params = dict(parse_qsl(parsed.query))
		filename = params.get('file', None)
		signature = params.get('signature', None)
		if not filename or not signature:
			self.send_response(HTTPStatus.BAD_REQUEST, "No filename or signature")

		h = hmac_sha1(SECRET, filename.encode())

		if insecure_compare(h, signature.encode()):
			self.send_response(HTTPStatus.OK, "You got it!")
		else:
			self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR, "Incorrect signature")

		self.end_headers()
		return True


def run_server():
	with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
		print("serving at port", PORT)
		httpd.serve_forever()


def time_f(f) -> int:
	start = time.time_ns()
	f()
	return int(time.time_ns() - start)


def attack_next_byte(signature, filename, sig_length) -> bytes:
	lows = {}
	observations = {}
	sample_size = 11  # Should be odd to make mean easier

	def f():
		attack_s = (signature + s.encode()).ljust(sig_length, b"\x00")
		requests.get(URL, params={'file': filename, 'signature': attack_s})

	for s in 'abcdefgh0123456789':
		for o in range(sample_size):
			t = time_f(f)
			observations.setdefault(s, []).append(t)

	for c, timings in observations.items():
		s_timings = list(sorted(timings))
		lows[str(c)] = s_timings[0]

	lowest = list(reversed(sorted(lows.items(), key=lambda x: x[1])))[0][0]
	return lowest.encode()


class TestChallenge32(unittest.TestCase):
	p = None

	@classmethod
	def setUpClass(cls) -> None:
		cls.p = Process(target = run_server)
		cls.p.start()
		time.sleep(1)
		pass

	@classmethod
	def tearDownClass(cls) -> None:
		cls.p.terminate()

	@unittest.skip
	def test_run_server_make_requests(self):
		filename = 'root.exe'
		print(hmac_sha1(SECRET, filename.encode()))
		# First guess the length
		sig_length = len(hmac_sha1(b'dummy', b'dummy'))
		signature = b''
		for i in range(sig_length):
			# Attacking the ith byte
			b = attack_next_byte(signature, filename, sig_length)
			signature += b

		r = requests.get(URL, params={'file': filename, 'signature': signature})
		print(signature)
		print(hmac_sha1(SECRET, filename.encode()))
		self.assertEqual(r.status_code, 200)

	def test_hmac(self):
		h = hmac_sha1(b"key", b"The quick brown fox jumps over the lazy dog")
		self.assertEqual(h, b'de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9')

