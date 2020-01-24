#!/usr/bin/env python3

# Standalone script that does not interface with Gnome NetworkManager

import requests
import bs4

sess = requests.Session()
portal_html = sess.get("http://detectportal.firefox.com").text
if portal_html.startswith("success"):
    return

tree = bs4.BeautifulSoup(portal_html, "html.parser")
postdata = {}
for inp in tree.find_all("input"):
    if not "name" in inp.attrs:
        continue
    postdata[inp["name"]] = inp["value"]

sess.post("https://railnet.oebb.at/connecttoweb", data=postdata)
