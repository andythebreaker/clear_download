import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import requests
from bs4 import BeautifulSoup
import urllib
import sys
import wget
import re
import os
import csv
import subprocess
import glob
from PIL import Image

class ClearNotebooksScraper:
    def __init__(self, note_id, viewDebug=False):
        self.note_id = note_id
        self.viewDebug = viewDebug

    def safe_file_name(self,file_name, os_type):
        # Remove leading/trailing whitespaces
        file_name = file_name.strip()

        # Replace invalid characters based on the operating system
        if os_type.lower() == "posix":#linux":
            file_name = re.sub(r'[/\?<>\\:\*\|"]', '', file_name)
        elif os_type.lower() == "nt":#windows":
            file_name = re.sub(r'[\\/:\*\?"<>\|]', '', file_name)
        else:
            raise ValueError("Invalid operating system type.")

        return file_name

    def remove_any_kind_of_new_line(self,str_):
        cleaned_string = re.sub(r'\s+', ' ', str_)
        return cleaned_string


    def scrape_clear_notebooks(self):

    #create dir "./build"
        if self.viewDebug:
            print("=====create dir ./build=====")
        if not os.path.exists("./build"):
            os.makedirs("./build")

        # !important! remove the code segment, due to cause bug
        # # Define the directory where you want to delete files
        # directory = "."
        # # Define a list of file extensions to delete
        # extensions_to_delete = ['png', 'jpg', 'jpeg', 'webm']
        # # Iterate over the specified extensions and delete the corresponding files
        # for extension in extensions_to_delete:
        #     file_pattern = os.path.join(directory, f'*.{extension}')
        #     files_to_delete = glob.glob(file_pattern)
        #     for file in files_to_delete:
        #         try:
        #             os.remove(file)
        #             print(f"Deleted {file}")
        #         except OSError as e:
        #             print(f"Error deleting {file}: {e}")

        if self.viewDebug:
            print("Deletion process complete.")

        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        pre = "https://www.clearnotebooks.com/zh-TW/notebooks/"
        ind = self.note_id
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
        info_time = soup0.find_all("time")
        try:
            notebook_category_grade__btn = soup0.find("a", {"class": "notebook-category-grade__btn"}).text
        except AttributeError:
            notebook_category_grade__btn = 'X'

        try:
            notebook_category_school_year__btn = soup0.find("a", {"class": "notebook-category-school-year__btn"}).text
        except AttributeError:
            notebook_category_school_year__btn = 'X'

        try:
            notebook_category_subject__btn = soup0.find("a", {"class": "notebook-category-subject__btn"}).text
        except AttributeError:
            notebook_category_subject__btn = 'X'

        tosumup=ttl+','+info_time[0].text+','+info_time[1].text+','+notebook_category_grade__btn+','+notebook_category_school_year__btn+','+notebook_category_subject__btn
        if self.viewDebug:
            print(tosumup)
        #workflow
        # Open the CSV file in append mode
        import csv

        # Assuming 'ind' and 'ttl' are defined elsewhere in your code
        with open(ind + '.csv', 'a', newline='', encoding='utf-8') as csvfile:
            # Create a CSV writer object
            csvwriter = csv.writer(csvfile)

            # Write the text to the CSV file
            csvwriter.writerow([ttl,info_time[0].text,info_time[1].text,notebook_category_grade__btn,notebook_category_school_year__btn,notebook_category_subject__btn])


        if self.viewDebug:
            print(f"Text '{ttl}' appended to {ind} successfully.")

        if self.viewDebug:
            print("=====")
        for objc in count:
            if self.viewDebug:
                print("=====")
                print(ci)
                print("=====")
            rq = picP + ind + pag + str(ci)
            r = requests.get(rq)  # Retrieve web page data
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, "html.parser")
            images = soup.findAll('img')
            #iurl = images[0]['src']
            iname = ttl + str(ci) + subjpg
            try:
                iurl = images[0]['src']
                filename = wget.download(iurl, self.remove_any_kind_of_new_line(self.safe_file_name(iname,os.name)))
                if self.viewDebug:
                    print("@")
            except:
                filename = wget.download('https://raw.githubusercontent.com/andythebreaker/clear_download/workflow/eof404.jpg', self.remove_any_kind_of_new_line(self.safe_file_name(iname,os.name)))
                if self.viewDebug:
                    print('[hotfix]https://github.com/andythebreaker/clear_download/issues/3')
                pass
            ci = ci + 1
        
        # Get a list of all .jpg files in the current directory
        jpg_files = [file for file in os.listdir() if file.endswith(".jpg")]

        # Iterate through the list of .jpg files
        for jpg_file in jpg_files:
            # Open the .jpg image
            with Image.open(jpg_file) as img:
                # Get the base filename (without extension)
                base_filename, _ = os.path.splitext(jpg_file)

                # Save the image as .png with the same name
                png_filename = base_filename + ".png"
                img.save(png_filename, "PNG")

            # Remove the original .jpg file
            os.remove(jpg_file)

        if self.viewDebug:
            print("Conversion and deletion complete.")
        # Define the command you want to execute
        command = ["node", "genpdf.js", ".", "./build", str(ind),f'{ttl}']

        # Run the command using subprocess
        subprocess.run(command, check=True)

if __name__ == "__main__":

    # Retrieve command-line arguments
    args = sys.argv
    note_id = ""

    # Parse command-line arguments
    for arg in args:
        if "--id=" in arg:
            note_id = arg.split("=")[1]
        elif arg == "--debug":
            viewDebug = True

    # Prompt for input if note_id is not provided as a command-line argument
    if not note_id:
        note_id = input("number of clear note: ")

    scraper = ClearNotebooksScraper(note_id, viewDebug)
    scraper.scrape_clear_notebooks()

