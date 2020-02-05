#!/usr/bin/env python3

# Script for use with Gnome NetworkManager

import requests
import bs4
import sys
import os

def connect():
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

    action_url = tree.find("form")["action"]
    sess.post(action_url, data=postdata)

if sys.argv[2] == "up" and os.environ["CONNECTION_ID"] == "OEBB":
    connect()
