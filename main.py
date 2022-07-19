import os
import sys
from time import sleep

#colors
RED = "\033[1;31m"
GREEN = "\033[0;32m"


list_check = ["x-vtex-api-apptoken", "x-vtex-api-appkey", "vtexappkey-"]
value = 0

print("Analising code...\n")

for x in list_check:
    req = os.popen('egrep -nr "%s" * | grep -v grep | grep -v "main.py" '%(x)).read()
    if x in req:
        print("\033[3;37;40mFinded in code \033[0;37;40m  \n")
        print(req)
        value = value + 1

if value > 0:
    sys.exit(1)
else:
    print(GREEN + "Pass")
    sys.exit(0)