import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import requests
from bs4 import BeautifulSoup
import urllib
import sys
import wget
import re
from py_web_clear import ClearNotebooksScraper

class ClearUsrScraper:
    def __init__(self, usr_id):
        self.usr_id = usr_id
        self.ntList=[]
        self.CONSTcn="https://www.clearnotebooks.com"

    def re_clusr(self,test_str):
        print("=====fetch=====")
        regex = r"\"path\":\"/zh-TW/notebooks/(\d+)\""

        matches = re.finditer(regex, test_str)

        for matchNum, match in enumerate(matches, start=1):
            
            print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
            
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
                self.ntList.append(match.group(groupNum))
        self.re_nx(test_str)

    def re_nx(self,test_str):
        print("=====next=====")
        regex = r"<a class=\"boxed\" href=\"(/zh-TW/authors/\d+/explorer/notebooks\?author_id=\d+&amp;offset=\d+)\">\d+</a><span class='pagination-info'>"
        matches = re.search(regex, test_str)

        if matches:
            print ("Match was found at {start}-{end}: {match}".format(start = matches.start(), end = matches.end(), match = matches.group()))
            
            for groupNum in range(0, len(matches.groups())):
                groupNum = groupNum + 1
                print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = matches.start(groupNum), end = matches.end(groupNum), group = matches.group(groupNum)))
                self.re_clusr(self.wget_me(f'{self.CONSTcn}{matches.group(groupNum)}'))

    def wget_me(self,url):
        print("=====wget=====")
        url = url
        response = requests.get(url)
        return response.text

    def scrape_clear_usr(self):
        print("=====get user notes (main) =====")
        url = f'{self.CONSTcn}/zh-TW/authors/{self.usr_id}/explorer/notebooks'
        content=self.wget_me(url)
        self.re_clusr(content)
        for itm in self.ntList:
            scraper = ClearNotebooksScraper(itm)
            scraper.scrape_clear_notebooks()


if __name__ == "__main__":
    # Retrieve command-line arguments
    args = sys.argv
    usr_id = ""

    # Parse command-line arguments
    for arg in args:
        if "--user=" in arg:
            usr_id = arg.split("=")[1]

    # Prompt for input if note_id is not provided as a command-line argument
    if not usr_id:
        usr_id = input("Enter clear user id: ")

    scraper = ClearUsrScraper(usr_id)
    scraper.scrape_clear_usr()
