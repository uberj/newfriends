import unittest
import string
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


def insecure_compare(hmac: bytes, signature: bytes):
    if len(hmac) != len(signature):
        return False

    for a, b in zip(hmac, signature):
        if a != b:
            return False
        time.sleep(0.05)

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


class TestChallenge31(unittest.TestCase):
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

    def test_run_server_make_requests(self):
        filename = 'root.exe'
        # First guess the length
        sig_length = len(hmac_sha1(b'dummy', b'dummy'))
        signature = b''
        for i in range(sig_length):
            longest = (0, -1)
            # Attacking the ith byte
            for s in 'abcdefgh0123456789':
                def f():
                    attack_s = (signature + s.encode()).ljust(sig_length, b"\x00")
                    requests.get(URL, params={'file': filename, 'signature': attack_s})
                t = time_f(f)
                if t > longest[0]:
                    longest = (t, s.encode())

            signature += longest[1]

        r = requests.get(URL, params={'file': filename, 'signature': signature})
        self.assertEqual(r.status_code, 200)

    def test_hmac(self):
        h = hmac_sha1(b"key", b"The quick brown fox jumps over the lazy dog")
        self.assertEqual(h, b'de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9')

