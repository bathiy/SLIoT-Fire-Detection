from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)

# HTML form template
FORM_HTML = '''
<!doctype html>
<title>Configure Fire Detection</title>
<h2>📷 Fire Detection Setup</h2>
<form method=post>
  <label>Wi-Fi SSID:</label><br>
  <input type=text name=ssid required><br><br>

  <label>Wi-Fi Password:</label><br>
  <input type=password name=password required><br><br>

  <label>RTSP URL:</label><br>
  <input type=text name=rtsp_url required><br><br>

  <label>Firebase UID:</label><br>
  <input type=text name=uid required><br><br>

  <input type=submit value=Save>
</form>
'''

SUCCESS_HTML = '''
<!doctype html>
<title>Configured</title>
<h2>✅ Configuration Saved</h2>
<p>Your Raspberry Pi will now reboot and connect to your Wi-Fi to begin fire detection.</p>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ssid = request.form.get('ssid')
        password = request.form.get('password')
        rtsp_url = request.form.get('rtsp_url')
        uid = request.form.get('uid')

        if ssid and password and rtsp_url and uid:
            # Save to config.json
            config_data = {
                "ssid": ssid,
                "password": password,
                "rtsp_url": rtsp_url,
                "uid": uid
            }
            with open("config.json", "w") as f:
                json.dump(config_data, f)

            # Overwrite /etc/wpa_supplicant/wpa_supplicant.conf
            wifi_config = f"""
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="{ssid}"
    psk="{password}"
}}
"""
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
                f.write(wifi_config)

            # Reboot to switch from AP to Wi-Fi client
            os.system("sudo reboot")

            return render_template_string(SUCCESS_HTML)

    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
