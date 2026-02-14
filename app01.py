from flask import Flask, request, jsonify
from user_agents import parse
import os

app = Flask(__name__)

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@app.route("/")
def home():
    return "Device Login App Running"

@app.route("/login")
def login():

    ip_address = get_client_ip()

    ua_string = request.headers.get('User-Agent', '')   # ✅ FIXED
    ua = parse(ua_string)

    os_name = ua.os.family

    if ua.is_mobile:
        device_type = "Mobile"

    elif ua.is_tablet:
        device_type = "Tablet"

    elif ua.is_pc:
        laptop_keywords = ["Mac", "Mac OS", "Chrome OS"]

        if any(word in os_name for word in laptop_keywords):
            device_type = "Laptop"
        else:
            device_type = "Desktop PC"
    else:
        device_type = "Unknown"

    device_info = f"{ua.os.family} - {ua.browser.family}"

    return jsonify({
        "ip_address": ip_address,
        "device_type": device_type,
        "device_info": device_info
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
