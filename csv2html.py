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
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            vara=', '.join(row)
            print(vara)
            maintxt+="<tr><td>"+vara+"</td><td><a href=\"https://www.clearnotebooks.com/zh-TW/notebooks/"+csvFile_rm_FE+"\">"+csvFile_rm_FE+"</a></td></tr>"

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

#copy file "index.html" to "./build"
print("=====copy file index.html to ./build=====")
shutil.copy("index.html", "./build")
