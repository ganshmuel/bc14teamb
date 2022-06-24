from subprocess import STDOUT, check_output

def runTest(testPort):
    result=set()
    with open('Scripts/tests.sh', 'r') as fp:
        lines = (l for l in (line.strip() for line in fp) if l)
        cnt = 1
        codebuild = ''
        for line in lines:
            cmd = line.strip()
            if (not cmd.startswith('#')):
            
                if (cmd.endswith('\\')):
                    codebuild += cmd[:-1]
                    continue
                
                codebuild += cmd
                
                try:
                    codebuild = codebuild.replace("localhost", "3.68.253.241")
                    try:
                        codebuild = codebuild.replace("8080", testPort)
                    except:
                        codebuild = codebuild.replace("8081", testPort)
                    
                    status= check_output([codebuild],stderr = STDOUT, timeout = 2,shell=True).decode('utf-8').strip()
                    result.add(status)
                except:
                    print(f"failed on \"{codebuild}\"")
                    result.add(codebuild)
    
                codebuild = ''
    
    if (len(result) == 1 and list(result)[0] == "200"):
        return "success"
        
    else: 
        failes = list(result)
        return failes

       