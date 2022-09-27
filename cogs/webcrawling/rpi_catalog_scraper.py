# RPI Catalog Scraper
import requests
from bs4 import BeautifulSoup

from discord.ext import commands


# Fetches all of the course's
def soup_search(url):
    search_result = requests.get(url).text
    search_soup = BeautifulSoup(search_result, 'html.parser')

    return search_soup.find_all("a", {"style": "float:right",
                                         "href": "javascript:acalogPopup('/mime/download.?catoid=24&ftype=3&foid=', 'view_flashpoint', 770, 530, 'yes')"})


def find_course(course_list):
    for course in course_list:
        course_title = course.parent.h3.text.strip()
        course_id = course_title.split(" - ")[0].strip()
        course_subject = course_id.split(" ")[0].strip()
        course_number = course_id.split(" ")[1].strip()
        course_name = course_title.split(" - ")[1].strip()
        course_description = course.parent.text.replace(course_title,
                                                        "").strip()  # Order from top to bottom: Description, Prerequsites/Corequisites, When Offered, Cross Listed, Credit Hours
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

        print("----------------------------------")
        print(f"Course Subject: {course_subject}")
        print(f"Course Number: {course_number}")
        print(f"Course Name: {course_name}")
        print(f"Description: {course_description}")
        print(f"Course Prerequisites/Corequisites: {course_requisites}")
        print(f"Course Offered: {course_offered}")
        print(f"Course Crosslisted: {course_crosslisted}")
        print(f"Credit Hours: {course_credit_hours}")


if __name__ == "__main__":
    subject_code = "-1"  # -1 searches for all courses
    for page_number in range(1, 21):
        page_url = f"http://catalog.rpi.edu/content.php?" \
                   f"filter%5B27%5D={subject_code}" \
                   f"&filter%5B29%5D=&filter%5Bcourse_type%5D=" \
                   f"&filter%5Bkeyword%5D=" \
                   f"&filter%5B32%5D=1&filter%5Bcpage%5D={page_number}" \
                   f"&cur_cat_oid=24&expand=1&navoid=606&print=1&filter%5Bexact_match%5D=1#acalog_template_course_filter"

        find_course(soup_search(page_url))


