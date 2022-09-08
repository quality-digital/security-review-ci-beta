import os
import sys
from time import sleep
import requests
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

        repo = os.popen('git config --get remote.origin.url').read()
        access = repo.replace('git@github.com:', 'https://github.com/')
        url = "Forbideen"
        payload = '''
        {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Hardcode !",
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
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "<%s|View>"
                        }
                    }
                ]
            
        }
        '''%(repo.replace('git@github.com:ACCT-global/', '').replace('.git', ''), access, time())
        try:
            r = requests.post(url, data=payload)
            print(r.text)

        except Exception:
            print("Ocorreu um erro ao enviar msg para o Slack")

if value > 0:
    sys.exit(1)
else:
    print(GREEN + "Pass")
    sys.exit(0)
