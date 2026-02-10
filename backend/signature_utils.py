from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import os
from signature_utils import sign_data, verify_data

KEYS_DIR = "keys"
PRIVATE_KEY = os.path.join(KEYS_DIR, "private.pem")
PUBLIC_KEY = os.path.join(KEYS_DIR, "public.pem")

if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)

if not os.path.exists(PRIVATE_KEY):
    key = RSA.generate(2048)
    open(PRIVATE_KEY, "wb").write(key.export_key())
    open(PUBLIC_KEY, "wb").write(key.publickey().export_key())


def sign_data(data):
    private_key = RSA.import_key(open(PRIVATE_KEY, "rb").read())
    h = SHA256.new(data)
    signer = PKCS1_v1_5.new(private_key)
    return signer.sign(h)


def verify_data(data, signature):
    public_key = RSA.import_key(open(PUBLIC_KEY, "rb").read())
    h = SHA256.new(data)
    verifier = PKCS1_v1_5.new(public_key)
    return verifier.verify(h, signature)
