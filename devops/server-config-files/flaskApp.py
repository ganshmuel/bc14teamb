from re import sub
from flask import Flask , request, json
import subprocess
import time
from Scripts import mailing
from os.path import exists



app = Flask(__name__)

def loadPordEnv(branchName):
    subprocess.call(f"/test-env/exec-files/run-compose.sh {branchName}", shell=True)
    
def pullBranch(branchName):
    subprocess.call("/test-env/exec-files/pull-branch.sh " + branchName , shell=True)
    return True

def startTests(branchName, commiterMail):
    
    ip ="3.68.253.241:"
    if branchName == "weight":
        ip += "8084"
    elif branchName == "billing":
        ip += "8083"
         
    testFolder= f"/test-env/bc14teamb/{branchName}/tests"
    if not exists(f"{testFolder}/run_test.sh"):
        return f"{testFolder}/run_test.sh not found"
    
    subprocess.call(f"chmod +x {testFolder}/run_test.sh", shell=True)
    #subprocess.call(f" bash {testFolder}/run_test.sh {ip}" , shell=True)
    time.sleep(10)
    subprocess.run([f"{testFolder}/run_test.sh", ip]) 
    if not exists(f"./log-test.txt"):
        return f"./log-test.txt ---- not exist"
    
    with open(f"./log-test.txt") as logFile:
        res = logFile.readlines()
        if "true" in res[0]:
            cleanTestEnv()
            msg = f"Push {branchName} Passed the tests Successfully\n\n"
            loadPordEnv(branchName)
        else:
            msg = f"Push {branchName} Didn't Passed the tests\n\n"
        for line in res: 
                msg+=f"{line}\n"
        return msg
            
        
def cleanTestEnv():
    subprocess.call("/test-env/exec-files/down-compose.sh", shell=True)

def loadTestEnv(branchName):
    subprocess.call(f"/test-env/exec-files/run-compose.sh dev {branchName}", shell=True)
    return True    

@app.route("/test", methods=[ "POST"])
def test():
    branches = ["billing", "weight"]
    data = request.get_json()
    branchName =data["ref"].partition("refs/heads/")[2]  
    if branchName not in branches: 
        return f'{branchName} not suported to CR'
    commmiterMail =list(data["commits"])[0]["committer"]["email"]
    #pullBranch(branchName)
    loadTestEnv(branchName)
    stValue =startTests(branchName, commmiterMail)
    
    #mailing.sendMail(commmiterMail, "msg")
    return stValue 

@app.route("/somthing")
def somthing():
    return "ok"    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
