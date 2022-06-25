from re import sub
from flask import Flask , request, json
import subprocess 
from Scripts import mailing
from os.path import exists



app = Flask(__name__)

def initiate_git():
    subprocess.call("/test-env/exec-files/init-git.sh", shell=True)

def loadPordEnv():
    subprocess.call("./run-compose.sh",shell=True)
    
def pullBranch(branchName):
    subprocess.call("/test-env/exec-files/pull-branch.sh " + branchName , shell=True)
    return True

def startTests(branchName, commiterMail):
    testFolder= f"/test-env/bc14teamb/{branchName}/tests"
    if not exists(f"{testFolder}/run_test.sh"):
        return f"{testFolder}/run_test.sh"
    
    loadTestEnv()
    
    subprocess.call(f"chmod +x {testFolder}/run_test.sh", shell=True)
    subprocess.call(f" bash {testFolder}/run_test.sh {testFolder}" , shell=True)
    
    if not exists(f"./log-test.txt"):
        return f"./log-test.txt ---- not exist"
    
    with open(f"./log-test.txt") as logFile:
        res = logFile.readlines()
        if "true" in res[0]:
            #deploy
            #mailing.sendMail(commiterMail, res.__str__() )
            #live test
            return "pass"
        else:
            return ("faild", res).__str__()
            #mailing.sendMail(commiterMail, res.__str__() )
            
        
def cleanTestEnv():
    subprocess.call("/test-env/exec-files/down-compose.sh", shell=True)

def loadTestEnv():
    subprocess.call("/test-env/exec-files/run-compose.sh dev", shell=True)
    return True    

@app.route("/test", methods=[ "POST"])
def test():
    branches = ["billing", "weight"]
    data = request.get_json()
    branchName =data["ref"].partition("refs/heads/")[2]  
    if branchName not in branches: 
        return f'{branchName} not suported to CR'
    commmiterMail =list(data["commits"])[0]["committer"]["email"]
    pullBranch(branchName)
    stValue =startTests(branchName, commmiterMail)
    cleanTestEnv()
    #mailing.sendMail(commmiterMail, "msg")
    return {"st-value":stValue} 

@app.route("/somthing")
def somthing():
    return "ok"    

if __name__ == "__main__":
    initiate_git()
    app.run(host="0.0.0.0", port=5000)
