#!/usr/bin/env python3

# Standalone script that does not interface with Gnome NetworkManager

import requests
import bs4
import sys

sess = requests.Session()
portal_html = sess.get("http://detectportal.firefox.com").text
if portal_html.startswith("success"):
    sys.exit(0)

tree = bs4.BeautifulSoup(portal_html, "html.parser")
postdata = {}
for inp in tree.find_all("input"):
    if not "name" in inp.attrs:
        continue
    postdata[inp["name"]] = inp["value"]

action_url = tree.find("form")["action"]
response = sess.post(action_url, data=postdata)
sys.exit(0 if response.status_code == 200 else 1)
