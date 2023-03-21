import os
import sys
from time import sleep
from datetime import datetime

#colors
RED = "\033[1;31m"
GREEN = "\033[0;32m"

#date
def time():
  url = 'http://worldtimeapi.org/api/timezone/America/Sao_Paulo'
  resposta = requests.get(url)
  hora = datetime.fromisoformat(resposta.json()['datetime'])
  hora = hora.strftime("%H:%M:%S - %d/%m/%Y")
  return hora

list_check = ["vtexappkey-"]
value = 0

print("Analising code...\n")

for x in list_check:
    req = os.popen('egrep -nri "%s" * | grep -v grep | grep -v "main.py" | grep -v "list_check" '%(x)).read()
    if x in req:
        print("\033[3;37;40mFinded in code \033[0;37;40m  \n")
        print(req)
        value = value + 1

        try:
            import requests
            repo = os.popen('git config --get remote.origin.url').read()
            branch = os.popen('git branch').read()
            access = repo.replace('git@github.com:', 'https://github.com/')
            url = sys.argv[1]
            payload = '''
            {
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Found Vulnerability",
                                "emoji": true
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": "*Project:*\n%s"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "*When:* %s"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "*Branch:* \n%s"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "*Vuln:* \nHardcode"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "%s"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "%s"
                            }
                        }
                    ]
                
            }
            '''%(repo.replace('git@github.com:quality-digital/', '').replace('.git', ''), time(), branch, req, access)
            print(payload)
            os.system('echo "%s" | base64'%(sys.argv[1]))
            r = requests.post(url, data=payload)
            print(r.text)

        except Exception as e:
            print("Error send message for slack.")
            print('Log: '+ str(e))
             
########################################

if value > 0:
    sys.exit(1)
else:
    print(GREEN + "Pass")
    sys.exit(0)
