from re import sub
from flask import Flask , request, json
import subprocess 
from Scripts import mailing



app = Flask(__name__)

def initiate_git():
    subprocess.call("/test-env/exec-files/init-git.sh", shell=True)

def loadPordEnv():
    subprocess.call("./run-compose.sh",shell=True)
    
def pullBranch(branchName):
    subprocess.call("/test-env/exec-files/pull-branch.sh " + branchName , shell=True)
    return True

def startTests(branchName):
    pass

def loadTestEnv(branchName):
    subprocess.call("/test-env/exec-files/run-compose.sh " + branchName + " dev", shell=True)
    return True    

@app.route("/test", methods=[ "POST"])
def test():
    branches = ["billing", "weight"]
    data = request.get_json()
    branchName =data["ref"].partition("refs/heads/")[2]  
    if branchName not in branches: 
        return f'{branchName} not suported to CR'
    commmiterMail =list(data["commits"])[0]["committer"]["email"]
    pullBranch(branchName) and loadTestEnv(branchName)
    testLog = startTests(branchName)
    #mailing.sendMail(commmiterMail, testLog)
    return testLog.__str__()
    

if __name__ == "__main__":
    initiate_git()
    app.run(host="0.0.0.0", port=5000)
