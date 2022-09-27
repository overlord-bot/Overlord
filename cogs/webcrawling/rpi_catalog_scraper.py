# RPI Catalog Scraper
import requests
from bs4 import BeautifulSoup

from discord.ext import commands

subject_codes = ["-1", "CSCI"]  # add remaining codes later
page_number = "1"
for subject_code in subject_codes:
    url = f"http://catalog.rpi.edu/content.php?" \
          f"filter%5B27%5D={subject_code}" \
          f"&filter%5B29%5D=" \
          f"&filter%5Bcourse_type%5D=" \
          f"&filter%5Bkeyword%5D=" \
          f"&filter%5B32%5D=1&filter%5Bcpage%5D={page_number}" \
          f"&cur_cat_oid=24&expand=1&navoid=606&print=1&filter%5Bexact_match%5D=1#acalog_template_course_filter"
    print(url)

all_url = "http://catalog.rpi.edu/content.php?filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bcourse_type%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=24&expand=1&navoid=606&print=1&filter%5Bexact_match%5D=1#acalog_template_course_filter"
search_result = requests.get(all_url).text
search_soup = BeautifulSoup(search_result, 'html.parser')

courses = search_soup.find_all("a", {"style": "float:right",
                                     "href": "javascript:acalogPopup('/mime/download.?catoid=24&ftype=3&foid=', 'view_flashpoint', 770, 530, 'yes')"})

for course in courses:
    course_title = course.parent.h3.text.strip()
    course_description = course.parent.text.replace(course_title, "").strip()  # Order from top to bottom: Description, Prerequsites/Corequisites, When Offered, Cross Listed, Credit Hours
    course_credit_hours = "Unknown"
    course_crosslisted = "Not Crosslisted"
    course_offered = "Unknown"
    course_requisites = "None"

    if len(course_description.split("Credit Hours: ")) > 1:
        course_credit_hours = course_description.split("Credit Hours: ")[1].strip()
    course_description = course_description.split("Credit Hours: ")[0].strip()

    if len(course_description.split("Cross Listed: ")) > 1:
        course_crosslisted = course_description.split("Cross Listed: ")[1].strip()
    course_description = course_description.split("Cross Listed: ")[0].strip()

    if len(course_description.split("When Offered: ")) > 1:
        course_offered = course_description.split("When Offered: ")[1].strip()
    course_description = course_description.split("When Offered: ")[0].strip()

    if len(course_description.split("Prerequisites/Corequisites: ")) > 1:
        course_requisites = course_description.split("Prerequisites/Corequisites: ")[1].strip()
    course_description = course_description.split("Prerequisites/Corequisites: ")[0].strip()

    print(f"\n{course_title}")
    print(f"Description: {course_description}")
    print(f"Course Prerequisites/Corequisites: {course_requisites}")
    print(f"Course Offered: {course_offered}")
    print(f"Course Crosslisted: {course_crosslisted}")
    print(f"Credit Hours: {course_credit_hours}")



