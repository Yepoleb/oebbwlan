#!/usr/bin/env python3

# Standalone script that does not interface with Gnome NetworkManager

import requests
import urllib.parse
import re
import sys

POST_DATA = 'request=%7B%22model%22%3A%22customers%22%2C%22method%22%3A%22loginOverLoginModule%22%2C%22formName%22%3A%22login_oneclicklogin%22%2C%22formData%22%3A%7B%22profiles_id%22%3A%222%22%2C%22policy_1%22%3A1%2C%22submit_login%22%3A%22Login%22%7D%2C%22requestType%22%3A%22formValidation%22%2C%22params%22%3A%7B%22formID%22%3A%22formLoginOneClickLogin_6%22%2C%22data%22%3A%7B%22profiles_id%22%3A%222%22%2C%22policy_1%22%3A1%2C%22submit_login%22%3A%22Login%22%7D%7D%2C%22countPageImpression%22%3Atrue%7D'
AJAX_URL = "https://portal-wab.oebb.at/Ajax/service/"
LOGIN_URL = "https://wab.oebb.at/login"

sess = requests.Session()
response = sess.head("http://detectportal.firefox.com")
if response.status_code == 200 and response.headers['Content-Length'] == "8":
    sys.exit(0)

sess.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"

wab = sess.get("https://wab.oebb.at/login")
ap_mac_url = re.search(r"https://'\+getHostname\(\)\+'(/.+)';", wab.text)
portal_url = "https://portal-wab.oebb.at" + ap_mac_url.group(1)
portal = sess.get(portal_url)
login_req = sess.post(AJAX_URL, data=POST_DATA, headers={
    'Accept': '*/*',
    'Accept-Language': 'de-AT,en-US;q=0.7,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://portal-wab.oebb.at',
    'Connection': 'keep-alive',
    'Referer': 'https://portal-wab.oebb.at/customer/login'
})
login_resp = login_req.json()
login_data = urllib.parse.urlencode({
    "username": login_resp["result"]["loginProcess"]["username"],
    "password": login_resp["result"]["loginProcess"]["password"]})
response = sess.post(LOGIN_URL, data=login_data)
sys.exit(0 if response.status_code == 200 else 1)
