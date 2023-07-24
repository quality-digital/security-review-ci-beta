import os
import sys
from datetime import datetime
import requests

# ANSI colors for terminal output
RED = "\033[1;31m"
GREEN = "\033[0;32m"

# List of sensitive tokens to check
list_check = ["vtexappkey-", "my_secret_token", "api_key", "password", "access_token",
              "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"]

# Function to get the current time
def get_time():
    """
    This function returns the current time in the timezone 'America/Sao_Paulo' 
    by making a GET request to the worldtimeapi.org API.

    Returns:
        str: Current time in the format "%H:%M:%S - %d/%m/%Y".
    """
    url = 'http://worldtimeapi.org/api/timezone/America/Sao_Paulo'
    resposta = requests.get(url)
    hora = datetime.fromisoformat(resposta.json()['datetime'])
    hora = hora.strftime("%H:%M:%S - %d/%m/%Y")
    return hora

def analyze_code_for_tokens():
    """
    This function analyzes the codebase for the presence of any sensitive tokens defined 
    in the 'list_check' list. If found, it sends a Slack message using the 
    'send_slack_message' function. 

    Tokens are searched excluding lines from "main.py" and "list_check" using the 
    'egrep' and 'grep' Linux commands.
    """
    print("Analyzing code for sensitive tokens...\n")
    found_warnings = False

    for token in list_check:
        cmd = f'egrep -nri "{token}" * | grep -v grep | grep -v "main.py" | grep -v "list_check"'
        req = os.popen(cmd).read()

        if token in req:
            print(f"\033[3;37;40mFound '{token}' in code \033[0;37;40m\n")
            print(req)
            
            warning_message = "Warning: Sensitive token found. Sending message to Slack.\033[0;37;40m"
            
            if token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9":
                warning_message = "\033[3;33;40mWarning: JWT identified. Sending message to Slack.\033[0;37;40m"

            found_warnings = True
            print(warning_message)
            send_slack_message("<SLACK_WEBHOOK_URL>", token)

    print_status_message(found_warnings)

def print_status_message(found_warnings):
    """
    This function prints a status message in the terminal based on the result of the 
    code analysis. The message is colored red if warnings are found, and green if no 
    warnings are found.

    Args:
        found_warnings (bool): Whether warnings have been found during the code analysis.
    """
    if found_warnings:
        print(RED + "Warnings found. Check Slack for details.")
    else:
        print(GREEN + "No warnings found.")

def send_slack_message(webhook_url, token):
    """
    This function sends a Slack message with a predefined payload to a specified 
    webhook URL. The payload includes the project details and a message indicating 
    that a sensitive token has been found.

    Args:
        webhook_url (str): The Slack webhook URL to send the message to.
        token (str): The sensitive token that was found in the codebase.
    """
    try:
        repo = os.popen('git config --get remote.origin.url').read().strip()
        branch = os.popen('git branch').read().strip()
        access = repo.replace('git@github.com:', 'https://github.com/')

        payload = generate_payload(repo, branch, access, token)

        r = requests.post(webhook_url, json=payload)
        print(r.text)

    except Exception as e:
        print("Error sending message to Slack.")
        print('Log: ' + str(e))

def generate_payload(repo, branch, access, token):
    """
    This function generates a payload for the Slack message. 

    Args:
        repo (str): The URL of the git repository.
        branch (str): The branch name in the git repository.
        access (str): The access URL of the git repository.
        token (str): The sensitive token that was found in the codebase.

    Returns:
        dict: The payload to be sent in the Slack message.
    """
    return {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": "Found Vulnerability", "emoji": True}},
            {"type": "section", "fields": [
                {"type": "mrkdwn", "text": f"*Project:*\n{repo.replace('git@github.com:quality-digital/', '').replace('.git', '')}"},
                {"type": "mrkdwn", "text": f"*When:* {get_time()}"},
                {"type": "mrkdwn", "text": f"*Branch:* \n{branch}"},
                {"type": "mrkdwn", "text": "*Vuln:* \nHardcode"}]},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"Found sensitive token: {token}"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": access}}
        ]
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Webhook URL not provided.")
        print("Usage: python main.py <webhook_url>")
        sys.exit(1)

    analyze_code_for_tokens()
