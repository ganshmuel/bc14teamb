from re import sub
from flask import Flask , request, json
import subprocess 
app = Flask(__name__)

def initiate_git():
    subprocess.call("/test-env/exec-files/init-git.sh", shell=True)

def runCompose():
    subprocess.call("./run-compose.sh",shell=True)
    
def pullBranch(branchName):
    subprocess.call("/test-env/exec-files/pull-branch.sh " + branchName , shell=True)
    return True

def runTest(branchName):
    subprocess.call("/test-env/exec-files/run-compose.sh " + branchName + " dev", shell=True)
    return True    

@app.route("/test", methods=[ "POST"])
def test():
    data = request.get_json()
    print(data["ref"])   
    #pullBranch(branchName) and runTest(branchName)
    return "OK"

if __name__ == "__main__":
    initiate_git()
    app.run(host="0.0.0.0", port=5000)
