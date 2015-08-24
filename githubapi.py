import getpass
import requests
import json
import traceback, sys

gh_username = raw_input('GitHub username: ')
gh_password = getpass.getpass('GitHub password: ')
# payload = json.dumps({'scopes': []})
payload = json.dumps({'scopes': [],'note': "python test auth"})

gh_response = requests.post('https://api.github.com/authorizations', auth=(gh_username, gh_password), data=payload)
try:
    # print gh_response.json()['token']
    #print gh_response.json()
    print gh_response.json()['token']
except: 
    # traceback.print_tb()
    print (traceback.format_exc())
    print ("Traceback printed.")