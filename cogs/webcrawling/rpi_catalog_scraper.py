# RPI Catalog Scraper
import requests
from bs4 import BeautifulSoup

from discord.ext import commands

subject_codes = ["-1", "CSCI"]  # add remaining codes later

for subject_code in subject_codes:
    url = f"http://catalog.rpi.edu/content.php?" \
          f"filter%5B27%5D={subject_code}" \
          f"&filter%5B29%5D=" \
          f"&filter%5Bcourse_type%5D=" \
          f"&filter%5Bkeyword%5D=" \
          f"&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=24&expand=1&navoid=606&print=1&filter%5Bexact_match%5D=1#acalog_template_course_filter"
    print(url)

cs_url = "http://catalog.rpi.edu/content.php?filter%5B27%5D=CSCI&filter%5B29%5D=&filter%5Bcourse_type%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=24&expand=1&navoid=606&print=1&filter%5Bexact_match%5D=1#acalog_template_course_filter"
search_result = requests.get(cs_url).text
search_soup = BeautifulSoup(search_result, 'html.parser')

courses = search_soup.find_all("a", {"style": "float:right",
                                     "href": "javascript:acalogPopup('/mime/download.?catoid=24&ftype=3&foid=', 'view_flashpoint', 770, 530, 'yes')"})

for course in courses:
    course_title = course.parent.h3.text
    course_data = course.parent.text.replace(course_title, "").strip()
    course_credit_hours = "Not Available"
    if len(course_data.split("Credit Hours: ")) > 1:
        course_credit_hours = course_data.split("Credit Hours: ")[1]

    print(course_title)
    print(course_data)
    print(course_credit_hours)

