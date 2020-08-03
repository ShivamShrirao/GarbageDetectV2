from time import sleep
import requests
import sys

API_ENDPOINT = "http://annotate.ret2rop.com:31896/monitoring/"
uid = sys.argv[1]
data = {"uid": uid, "auth-token": "ENTER_AUTH_TOKEN"}


while True:
	r = requests.post(url = API_ENDPOINT, data = data)
	print(r)
	sleep(60)