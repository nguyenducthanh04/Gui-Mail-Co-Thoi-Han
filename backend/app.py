from flask import Flask, request, jsonify, render_template, send_from_directory, redirect
from sender_logic import create_packet
from receiver_logic import process_packet
from datetime import datetime
import json, os, pytz, threading

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("sender.html")

@app.route("/receiver")
def receiver():
    return render_template("receiver.html")

@app.route("/send", methods=["POST"])
def send():
    file = request.files.get("file")
    if not file:
        return jsonify(message="❌ Vui lòng chọn file"), 400
    file.save("email.txt")
    create_packet("email.txt", "transmission.json")

    if os.path.exists("feedback.json"):
        os.remove("feedback.json")

    return jsonify(message="✅ Đã tạo gói tin gửi!")

@app.route("/receive", methods=["POST"])
def receive():
    if not os.path.exists("transmission.json"):
        return jsonify(message="❗ Chưa có gói tin nào được gửi!"), 400

    ok, msg = process_packet("transmission.json")

    if ok:
        feedback = {
            "status": "received",
            "time": datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%d/%m/%Y %H:%M:%S")
        }
        with open("feedback.json", "w") as f:
            json.dump(feedback, f)

    return jsonify(message=msg)

@app.route("/files")
def list_files():
    files = []
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")

    for name in os.listdir("received_files"):
        path = os.path.join("received_files", name)
        if not os.path.isfile(path):
            continue

        timestamp = os.path.getmtime(path)
        received_dt = datetime.fromtimestamp(timestamp, tz=vn_tz)
        received_at = received_dt.strftime("%d/%m/%Y %H:%M:%S")

        files.append({
            "name": name,
            "received_at": received_at
        })

    return render_template("files.html", files=files)

@app.route("/download_file")
def download_file():
    name = request.args.get("name")
    path = os.path.join("received_files", name)

    if not os.path.exists(path):
        return "❌ File không tồn tại!", 404

    def delayed_delete(file_path):
        def delete():
            try:
                os.remove(file_path)
                print("✅ File đã bị xóa:", file_path)
            except Exception as e:
                print("❌ Không thể xóa file:", e)
        threading.Timer(2.0, delete).start()

    delayed_delete(path)
    return send_from_directory("received_files", name, as_attachment=True)

@app.route("/delete_file")
def delete_file():
    name = request.args.get("name")
    os.remove(f"received_files/{name}")
    return redirect("/files")

@app.route("/check_feedback", methods=["POST"])
def check_feedback():
    if os.path.exists("feedback.json"):
        with open("feedback.json") as f:
            data = json.load(f)
            return jsonify(received=True, time=data["time"])
    return jsonify(received=False)

@app.route("/check_packet")
def check_packet():
    if not os.path.exists("transmission.json"):
        return jsonify(has_packet=False)

    try:
        with open("transmission.json", "r") as f:
            p = json.load(f)
            exp = p.get("exp")
            exp_time = datetime.fromisoformat(exp.replace("Z", ""))
            now = datetime.utcnow()
            remaining = (exp_time - now).total_seconds()

            if remaining <= 0:
                return jsonify(has_packet=False)

            return jsonify(
                has_packet=True,
                remaining=int(remaining),
                exp=exp
            )
    except:
        return jsonify(has_packet=False)

if __name__ == "__main__":
    app.run(debug=True)
