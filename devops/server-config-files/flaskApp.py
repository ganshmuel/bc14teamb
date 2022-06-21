from re import sub
from flask import Flask
import subprocess

app = Flask(__name__)

def runCompose():
    subprocess.run(["bash","run-compose.sh"])


@app.route("/test")
def health():
    runCompose()
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
