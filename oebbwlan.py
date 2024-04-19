#!/usr/bin/env python3

# Standalone script that does not interface with Gnome NetworkManager

import requests
import bs4
import sys

verbose = any(arg in sys.argv[1:] for arg in ('-v', '--verbose'))

sess = requests.Session()
portal_html = sess.get("http://detectportal.firefox.com").text
if portal_html.startswith("success"):
    if verbose:
        print("Already online.")
    sys.exit(0)

tree = bs4.BeautifulSoup(portal_html, "html.parser")
postdata = {}
for inp in tree.find_all("input"):
    if not "name" in inp.attrs:
        continue
    postdata[inp["name"]] = inp["value"]

if verbose:
    print("Logging in as",
          ", ".join(k + "=" + v for k, v in postdata.items()))
action_url = tree.find("form")["action"]
response = sess.post(action_url, data=postdata)
if verbose:
    print(response.reason)
sys.exit(0 if response.status_code == 200 else 1)
