from re import sub
from flask import Flask , request
import subprocess

app = Flask(__name__)

def runCompose():
    subprocess.run(["bash","run-compose.sh"])

@app.route("/github-webhook", methods=['POST'])
def githubWebhook():
    
    return "ok"

@app.route("/test", method=["GET", "POST"])
def test():
    content = request.json
    branch = content['ref'].partition('refs/heads/')[2]
    repository = content['repository']['full_name']
    print(branch, repository)
    runCompose()
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
