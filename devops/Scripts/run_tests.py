import subprocess

# the program will open the shared tests script from the dev team and run the script
# with subprocess line by line ( excpeting "for each " line will do curl to the api and return 200 if succeed )
# the results will enter into a set and in the end will check if the set have only 1 var (200)
# if yes the tests are succeed if not the tests failed
result=set()
with open('tests/tests.sh', 'r') as fp:
    lines = fp.readlines()
    cnt = 1
    for index, line in enumerate(lines):
        if (cnt != 1 ):
            status= subprocess.run(["sh", "-c", line.strip()],stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
            result.add(status)
        cnt+=1

if (len(result) == 1 and list(result)[0] == "200"):
    print("success")

       

