#import system
import sys
import glob
import os
import csv
import re
from bs4 import BeautifulSoup
import requests
import wget
import urllib
import time
import random
import string
import shutil
import zipfile
import logging
#read file "htmlhd.txt"
with open("htmlhd.txt", "r") as f:
    htmlhd = f.read()
    print(htmlhd)
with open("htmlft.txt", "r") as f:
    htmlft = f.read()
    print(htmlft)

#main
maintxt = ""
maintxt+=htmlhd
#print list all .csv file in curren dir.
print("=====list all .csv file in curren dir.=====")
csvList = glob.glob('*.csv')
for csvFile in csvList:
    print(csvFile)
    #remove File extension
    csvFile_rm_FE = csvFile.replace(".csv", "")
    #print contant of .csv file
    print("=====print contant of .csv file=====")
    with open(csvFile, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            vara='</td><td>'.join(row)
            print(vara)
            maintxt+="<tr><td>"+vara+"</td><td><a href=\"https://www.clearnotebooks.com/zh-TW/notebooks/"+csvFile_rm_FE+"\">"+csvFile_rm_FE+"</a></td><td><a href=\"./"+csvFile_rm_FE+".pdf\">V</a></td></tr>"

#write file index.html
maintxt+=htmlft
with open("index.html", "w") as f:
    f.write(maintxt)

#remove all .csv file
print("=====remove all .csv file=====")
csvList = glob.glob('*.csv')
for csvFile in csvList:
    print(csvFile)
    os.remove(csvFile)

#create dir "./build"
print("=====create dir ./build=====")
if not os.path.exists("./build"):
    os.makedirs("./build")

import backburst1
import backburst2
import backburst3
import backburst4
import backburst5

#copy file "index.html" to "./build"
print("=====copy file index.html to ./build=====")
shutil.copy("index.html", "./build")

#rename file "index.html" to "table.html"
print("=====rename file index.html to table.html=====")
os.rename("index.html", "table.html")

backburst1.change_html_title("table.html")
backburst2.add_style_to_html_file("table.html")
backburst3.add_css_and_js_to_html("table.html")
backburst4.add_table_to_html("table.html")
backburst5.add_footer_to_html_file("table.html")

#copy file "table.html" to "./build"
print("=====copy file table.html to ./build=====")
shutil.copy("table.html", "./build")

#copy file "nega4.html" to "./build"
print("=====copy file nega4.html to ./build=====")
shutil.copy("nega4.html", "./build")
