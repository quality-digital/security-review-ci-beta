import os
import sys
from time import sleep
from datetime import datetime
import requests

# colors
RED = "\033[1;31m"
GREEN = "\033[0;32m"

# List of sensitive tokens to check
list_check = ["vtexappkey-", "my_secret_token", "api_key", "password", "access_token",
              "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"]

# Function to get the current time
def get_time():
    url = 'http://worldtimeapi.org/api/timezone/America/Sao_Paulo'
    resposta = requests.get(url)
    hora = datetime.fromisoformat(resposta.json()['datetime'])
    hora = hora.strftime("%H:%M:%S - %d/%m/%Y")
    return hora

def analyze_code_for_tokens():
    print("Analyzing code for sensitive tokens...\n")
    found_warnings = False

    for token in list_check:
        cmd = f'egrep -nri "{token}" * | grep -v grep | grep -v "main.py" | grep -v "list_check"'
        req = os.popen(cmd).read()

        if token in req:
            print(f"\033[3;37;40mFound '{token}' in code \033[0;37;40m\n")
            print(req)

            if token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9":
                found_warnings = True
                print("\033[3;33;40mWarning: JWT identified. Sending message to Slack.\033[0;37;40m")
                # Substitua '<SLACK_WEBHOOK_URL>' pelo seu URL do webhook do Slack
                send_slack_message("<SLACK_WEBHOOK_URL>", token)

            else:
                found_warnings = True
                print("\033[3;33;40mWarning: Sensitive token found. Sending message to Slack.\033[0;37;40m")
                # Substitua '<SLACK_WEBHOOK_URL>' pelo seu URL do webhook do Slack
                send_slack_message("<SLACK_WEBHOOK_URL>", token)

    if found_warnings:
        print(RED + "Warnings found. Check Slack for details.")
    else:
        print(GREEN + "No warnings found.")

def send_slack_message(webhook_url, token):
    try:
        repo = os.popen('git config --get remote.origin.url').read().strip()
        branch = os.popen('git branch').read().strip()
        access = repo.replace('git@github.com:', 'https://github.com/')

        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Found Vulnerability",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Project:*\n{repo.replace('git@github.com:quality-digital/', '').replace('.git', '')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*When:* {get_time()}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Branch:* \n{branch}"
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
                        "text": f"Found sensitive token: {token}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": access
                    }
                }
            ]
        }

        r = requests.post(webhook_url, json=payload)
        print(r.text)

    except Exception as e:
        print("Error sending message to Slack.")
        print('Log: ' + str(e))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Webhook URL not provided.")
        print("Usage: python main.py <webhook_url>")
        sys.exit(1)

    analyze_code_for_tokens()
