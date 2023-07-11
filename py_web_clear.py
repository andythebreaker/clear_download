import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import requests
from bs4 import BeautifulSoup
import urllib
import sys
import wget
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# Retrieve command-line arguments
args = sys.argv
note_id = ""

# Parse command-line arguments
for arg in args:
    if "--id=" in arg:
        note_id = arg.split("=")[1]

# Prompt for input if note_id is not provided as a command-line argument
if not note_id:
    note_id = input("number of clear note: ")

pre = "https://www.clearnotebooks.com/zh-TW/notebooks/"
ind = note_id
picP = "https://www.clearnotebooks.com/zh-TW/public_page?note_id="
pag = "&page="
subjpg = ".jpg"
totalP = pre + ind

r0 = requests.get(totalP)  # Retrieve web page data
r0.encoding = 'utf-8'
soup0 = BeautifulSoup(r0.text, "html.parser")
count = soup0.find_all("div", {"class": "pages__page__container"})
ci = 0
ttl = soup0.find("h1", {"class": "notebook__title"}).text
print(ttl)
print("=====")
for objc in count:
    print("=====")
    print(ci)
    print("=====")
    rq = picP + ind + pag + str(ci)
    r = requests.get(rq)  # Retrieve web page data
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    images = soup.findAll('img')
    iurl = images[0]['src']
    iname = ttl + str(ci) + subjpg
    try:
        filename = wget.download(iurl, iname)
    except:
        pass
    ci = ci + 1
