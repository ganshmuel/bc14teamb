import subprocess

# the program will open the shared tests script from the dev team and run the script
# with subprocess line by line ( excpeting "for each " line will do curl to the api and return 200 if succeed )
# the results will enter into a set and in the end will check if the set have only 1 var (200)
# if yes the tests are succeed if not the tests failed
result=set()
with open('tests/tests.sh', 'r') as fp:
    lines = (l for l in (line.strip() for line in fp) if l)
    cnt = 1
    codebuild = ''
    for line in lines:
        cmd = line.strip()
        if (cnt != 1 and not cmd.startswith('#')):
            if (cmd.endswith('\\')):
                codebuild += cmd[:-1]
                continue
            codebuild += cmd
            status= subprocess.run(["sh", "-c", codebuild],stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
            result.add(status)
            codebuild = ''
        cnt+=1

if (len(result) == 1 and list(result)[0] == "200"):
    print("success")
else: print("failed")
       