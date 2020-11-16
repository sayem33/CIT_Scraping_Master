import copy
import csv
import json
import re
import time
from pathlib import Path

import ast

# noinspection PyProtectedMember
from bs4 import Comment
from selenium import webdriver
from CustomMethods import DurationConverter, TemplateData
import bs4 as bs4
import requests
import os
from CustomMethods import DurationConverter as dura, DurationConverter
from CustomMethods import TemplateData


def durationo(p_word):
    if p_word:
        if 'year' in p_word.__str__().lower():
            value_conv = DurationConverter.convert_duration(p_word)
            duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
            duration_time = value_conv[1]

            if str(duration) == '1' or str(duration) == '1.0':
                course_data['Duration'] = duration
                course_data['Duration_Time'] = 'Year'
            elif 'month' in duration_time.__str__().lower():
                course_data['Duration'] = duration
                course_data['Duration_Time'] = 'Months'
            else:
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time

        elif 'months' in p_word.__str__().lower():
            value_conv = DurationConverter.convert_duration(p_word)
            duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
            duration_time = value_conv[1]
            course_data['Duration'] = duration
            course_data['Duration_Time'] = duration_time
        elif 'week' in p_word.__str__().lower():
            value_conv = DurationConverter.convert_duration(p_word)
            duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
            duration_time = value_conv[1]
            course_data['Duration'] = duration
            course_data['Duration_Time'] = duration_time
        elif 'day' in p_word.__str__().lower():
            value_conv = DurationConverter.convert_duration(p_word)
            duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
            course_data['Duration'] = duration
            course_data['Duration_Time'] = 'Days'

        else:
            course_data['Duration'] = ""
            course_data['Duration_Time'] = ''
    else:
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''
        course_data['Full_Time'] = ""
        course_data['Part_Time'] = ""

def tag_text(tag):
    return tag.get_text().__str__().strip()

def parseint(string):
    m = re.search(r"(\d*\.?\d*)", string)
    return m.group() if m else None


option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/International_course_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/CIT_International_courses_info.csv'

course_data_gg = []

course_data = {'Level_Code': '',
               'University': 'Canberra Institute of Technology',
               'City': 'Canberra',
               'Course': '',
               'Faculty': '',
               'Int_Fees': '',
               'Local_Fees': '',
               'Currency': 'AUD',
               'Currency_Time': 'Years',
               'Duration': '',
               'Duration_Time': 'Year(s)',
               'Full_Time': '',
               'Part_Time': '',
               'Prerequisite_1': 'IELTS',
               'Prerequisite_2': '',
               'Prerequisite_3': 'Equivalent ',
               'Prerequisite_1_grade_1': '5.5',
               'Prerequisite_2_grade_2': '',
               'Prerequisite_3_grade_3': 'Year 12',
               'Website': '',
               'Course_Lang': 'English',
               'Availability': 'A',
               'Description': '',
               'Career_Outcomes/path': '',
               'Country': 'Australia',
               'Online': '',
               'Offline': 'Yes',
               'Distance': '',
               'Face_to_Face': '',
               'Blended': '',
               'Remarks': ''}

possible_cities = {'Canberra': 'canberra',

                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"


level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels


# GET EACH COURSE LINK
for each_url in course_links_file:
    actual_cities = []

    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'html.parser')
    time.sleep(1)

# SAVE COURSE URL
    course_data['Website'] = pure_url

# SAVE COURSE TITLE

    course_info = []
    print(pure_url)

    title = soup.find('div', attrs={'class': 'text-row'}).find('p').next_element
    title = tag_text(title)
    #title = title.split(" | ", 1)
    course_info.append(title)
    course_data['Course'] = course_info[0].rsplit(" | ", 1)[0]
    #print(course_data['Course'])


# DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    #print(course_data['Level_Code'])

# DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i
    #print(course_data['Faculty'])

# COURSE DESCRIPTION
    if soup.find_all('div', class_='pr-md-5'):
        description = soup.find_all('p')
        #description = tag_text(description)
        d_description = description[0].text.strip().replace('\n', '')
        course_data['Description'] = d_description
        #print(d_description)


## CAREER OUTCOME
    a_tag = soup.find('a', class_='opener', text=re.compile('Likely Job Outcome', re.IGNORECASE))
    if a_tag:
        career_outcome_div = a_tag.find_next_sibling('div', class_='slide js-acc-hidden')
        p_list = career_outcome_div.find_all('p')
        for c in p_list:
            c_outcome = tag_text(c).replace('\n', '')
            course_data['Career_Outcomes/path'] = c_outcome
            #print(c_outcome)

# DURATION/Duration Time/FullTime/Parttime/

    avaialbility_list = []

    try:
        duration = soup.select('.fz-16 > li:nth-child(2) > div:nth-child(2) > div:nth-child(1) > p:nth-child(1) > strong:nth-child(1)')
        for dur in duration:
            course_detail = dur.text.rstrip()
            course_detail2 = DurationConverter.convert_duration(course_detail)

        # print(course_detail2)

        course_data['Duration'] = course_detail2[0]
        course_data['Duration_Time'] = course_detail2[1]
    except TypeError:
        course_data['Duration'] = 'N/A'
        course_data['Duration_Time'] = 'N/A'
    except Exception:
        course_data['Duration'] = 'N/A'
        course_data['Duration_Time'] = 'N/A'


    # print(course_data['Duration'])
    # print(course_data['Duration_Time'])

    # avaialbility_list.append(course_detail2)
    #
    # for data in avaialbility_list:
    #     if avaialbility_list:
    #
    #         if data.lower().find('full-time') != -1 and data.lower().find('part-time') != -1:
    #             course_data['Part_Time'] = 'Yes'
    #             course_data['Full_Time'] = 'Yes'
    #         elif data.lower().find('full time') != -1 or data.lower().find('full-time') != -1:
    #             course_data['Full_Time'] = 'Yes'
    #             course_data['Part_Time'] = ''
    #         elif data.lower().find('part time') != -1 or data.lower().find('part-time') != -1:
    #             course_data['Part_Time'] = 'Yes'
    #             course_data['Full_Time'] = ''
    #
    #     else:
    #             course_data['Part_Time'] = ''
    #             course_data['Full_Time'] = ''

# INTERNATIONAL FEES
    try:
        table = soup.select('span.cell:nth-child(2)')

        for t in table:

            fee = tag_text(t)
            fee = fee.replace(',', '')
            fee1 = str(re.findall(r'\$\d+(?:\.\d+)?', fee))
            Int_fee = fee1.replace('$', '').strip("[]").strip("''")
            course_data['Int_Fees'] = float(Int_fee)
            # print(Int_fee)
            # print(course_data['Int_Fees'])
            #print(", ".join(repr(e) for e in Int_fee))

    except ValueError:
        course_data['Int_Fees'] = ''

    except AttributeError:
        course_data['Int_Fees'] = ''

    #print(course_data, sep='\n')

# DUPLICATE ENTRIES with multiple cities for each city
#     for i in actual_cities:
#         course_data['City'] = possible_cities[i]
#         course_data_all.append(copy.deepcopy(course_data))
#     del actual_cities

 #---------------------------
#     # print(course_data)
    temp = course_data.copy()
    course_data_gg.append(temp)
#     # print(course_data_all)
#     # print(course_data_all)
#
# TABULATE OUR DATA

desired_order_list = ['Level_Code',
                      'University',
                      'City',
                      'Course',
                      'Faculty',
                      'Local_Fees',
                      'Int_Fees',
                      'Currency',
                      'Currency_Time',
                      'Duration',
                      'Duration_Time',
                      'Full_Time',
                      'Part_Time',
                      'Prerequisite_1',
                      'Prerequisite_2',
                      'Prerequisite_3',
                      'Prerequisite_1_grade_1',
                      'Prerequisite_2_grade_2',
                      'Prerequisite_3_grade_3',
                      'Website',
                      'Course_Lang',
                      'Availability',
                      'Description',
                      'Career_Outcomes/path',
                      'Country',
                      'Online',
                      'Offline',
                      'Distance',
                      'Face_to_Face',
                      'Blended',
                      'Remarks']


with open(csv_file, 'w', encoding='utf-8', newline='\n') as output_file:
    dict_writer = csv.DictWriter(output_file, desired_order_list)
    dict_writer.writeheader()
    for course in course_data_gg:
        dict_writer.writerow(course)


with open(csv_file, 'r', encoding='utf-8') as infile, open('CIT_International_courses_ordered.csv', 'w', encoding='utf-8',
                                                           newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)



