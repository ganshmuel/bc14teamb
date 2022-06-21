from re import sub
from flask import Flask , request, json
import subprocess 
app = Flask(__name__)

def runCompose():
    subprocess.call("./run-compose.sh",shell=True)
    
@app.route("/github-webhook", methods=['POST'])
def githubWebhook():
    
    return "ok"

@app.route("/deploy", methods=["GET", "POST"])
def deploy():
    if request.method == 'POST':
        request_json = request.json        # print the received notification
        print('Payload: ')
        # Change from original - remove the need for function to print
        print(json.dumps(request_json,indent=4))
        runCompose()
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
