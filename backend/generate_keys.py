from Crypto.PublicKey import RSA
import os

os.makedirs("backend/keys", exist_ok=True)

def generate(name):
    key = RSA.generate(2048)
    open(f"backend/keys/{name}_private.pem", "wb").write(key.export_key())
    open(f"backend/keys/{name}_public.pem", "wb").write(key.publickey().export_key())

generate("sender")
generate("receiver")

print("🔐 Khóa RSA đã được tạo.")
