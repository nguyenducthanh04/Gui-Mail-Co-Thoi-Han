import base64, json, os, re
from datetime import datetime
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512

def unpad(data):
    return data[:-data[-1]]
def process_packet(in_file):
    print("Receiver: Hello!")
    print("Sender: Ready!")

    try:
        with open(in_file, "r") as f:
            p = json.load(f)
    except Exception:
        return False, "❌ Không thể đọc gói tin!"

    try:
        # 1. Lấy dữ liệu từ gói tin
        iv = base64.b64decode(p["iv"])
        cipher = base64.b64decode(p["cipher"])
        ekey = base64.b64decode(p["ekey"])
        sig = base64.b64decode(p["sig"])
        metadata = p["metadata"]
        exp = p["exp"]
        expected_hash = p["hash"]

        # 2. Kiểm tra thời hạn
        if datetime.utcnow() > datetime.fromisoformat(exp.replace("Z", "")):
            return False, "❌ Hết hạn!"

        # 3. Kiểm tra hash
        h = SHA512.new(iv + cipher + exp.encode()).hexdigest()
        if h != expected_hash:
            return False, "❌ Kiểm tra hash thất bại!"

        # 4. Kiểm tra chữ ký
        sender_public = RSA.import_key(open("backend/keys/sender_public.pem", "rb").read())
        pkcs1_15.new(sender_public).verify(SHA512.new(metadata.encode()), sig)

        # 5. Giải mã session key và nội dung
        receiver_private = RSA.import_key(open("backend/keys/receiver_private.pem", "rb").read())
        session_key = PKCS1_v1_5.new(receiver_private).decrypt(ekey, None)

        aes = AES.new(session_key, AES.MODE_CBC, iv)
        plaintext = unpad(aes.decrypt(cipher))

        # 6. Lưu file đã giải mã vào thư mục quản lý
        os.makedirs("received_files", exist_ok=True)
        filename_only = metadata.split(":")[0]
        filename_only = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename_only)  # loại bỏ ký tự lạ

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename_only}"
        out_file = os.path.join("received_files", safe_filename)

        with open(out_file, "wb") as f:
            f.write(plaintext)

        # ✅ XÓA GÓI TIN SAU KHI GIẢI MÃ
        os.remove(in_file)

        return True, f"✅ Giải mã thành công! Đã lưu: {out_file}"

    except ValueError:
        return False, "❌ Chữ ký không hợp lệ!"
    except Exception as e:
        return False, f"❌ Lỗi xử lý: {str(e)}"
