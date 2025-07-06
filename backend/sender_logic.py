import base64, json
from datetime import datetime, timedelta
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512

def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len]) * pad_len

def create_packet(input_file, output_file):
    print("Sender: Hello!")
    print("Receiver: Ready!")

    data = open(input_file, "rb").read()
    data = pad(data)

    session_key = get_random_bytes(16)
    iv = get_random_bytes(16)

    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(data)

    exp = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
    metadata = f"{input_file}|{exp}"
    h = SHA512.new(iv + ciphertext + exp.encode()).hexdigest()

    sender_private = RSA.import_key(open("backend/keys/sender_private.pem", "rb").read())
    sig = pkcs1_15.new(sender_private).sign(SHA512.new(metadata.encode()))

    receiver_public = RSA.import_key(open("backend/keys/receiver_public.pem", "rb").read())
    enc_session_key = PKCS1_v1_5.new(receiver_public).encrypt(session_key)

    packet = {
        "iv": base64.b64encode(iv).decode(),
        "cipher": base64.b64encode(ciphertext).decode(),
        "hash": h,
        "sig": base64.b64encode(sig).decode(),
        "ekey": base64.b64encode(enc_session_key).decode(),
        "exp": exp,
        "metadata": metadata
    }

    with open(output_file, "w") as f:
        json.dump(packet, f, indent=2)
