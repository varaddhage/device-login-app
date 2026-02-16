from flask import Flask, request, jsonify
from user_agents import parse
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()

    if request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")

    return request.remote_addr

def detect_device(ua):

    os_name = ua.os.family

    if ua.is_mobile:

        if "Android" in os_name:
            return "Android Mobile"

        if "iOS" in os_name or "iPhone" in os_name:
            return "iPhone"

        return "Mobile"

    if ua.is_tablet:

        if "iPad" in os_name:
            return "iPad"

        return "Tablet"

    if ua.is_pc:

        laptop_os_keywords = ["Mac OS", "Chrome OS"]

        if any(word in os_name for word in laptop_os_keywords):
            return "Laptop"

        if "Windows" in os_name:
            return "Desktop PC"

        return "Computer"

    return "Unknown"


@app.route("/")
def home():
    return "Advanced Device Login App Running 🚀"


@app.route("/login")
def login():

    ip_address = get_client_ip()

    ua_string = request.headers.get("User-Agent", "")
    ua = parse(ua_string)

    device_type = detect_device(ua)

    device_info = f"{ua.os.family} - {ua.browser.family}"

    return jsonify({
        "ip_address": ip_address,
        "device_type": device_type,
        "device_info": device_info
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

