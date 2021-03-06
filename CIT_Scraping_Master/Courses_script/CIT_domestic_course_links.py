"""Description:
    * author: Sayem Rahman
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 02-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
from urllib.parse import urljoin
import os
import requests
import bs4
import bs4 as bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
# selenium web driver
# we need the Chrome driver to simulate JavaScript functionality
# thus, we set the executable path and driver options arguments
# ENSURE YOU CHANGE THE DIRECTORY AND EXE PATH IF NEEDED (UNLESS YOU'RE NOT USING WINDOWS!)

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

course_links = []
url = 'https://cit.edu.au/study/course_guide/az_courses?result_63050_result_page='




# LINK EXTRACTOR
def fetch_url(url):
    # print(url)
    browser.get(url)
    soup = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')
    each_courses_links = [tag['href'] for tag in soup.select('p a[href^="https://cit.edu.au/courses/"]')]
    # print(*each_courses_links, sep='\n')
    course_links.extend(each_courses_links)



#iterate through all the pages
for i in range(1, 4):
    # url = url + str(i)
    fetch_url(url + str(i))

# print(*course_links, sep='\n')



# SAVE LINKS TO FILE
course_links_file_path = os.getcwd().replace('\\', '/') + '/course_links.txt'
course_links_file = open(course_links_file_path, 'w')

# print(course_links)
for i in course_links:
    print(i)
    # print(i.strip())
    # course_links_file.write(i.strip() + '\n')
    if i is not None and i != "" and i != "\n":
        if i == course_links[-1]:
            course_links_file.write(i.strip())
        else:
            course_links_file.write(i.strip()+'\n')
course_links_file.close()
