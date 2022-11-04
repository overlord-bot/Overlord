# RPI Catalog Scraper
import requests
from bs4 import BeautifulSoup
import time  # for calculating runtime
import json


# Finds all courses in an url based on its first child's "a" tag attributes
def soup_search(url):
    search_data = requests.get(url).text
    search_soup = BeautifulSoup(search_data, 'html.parser')
    course_data = search_soup.find_all("a", {"style": "float:right", "href": "javascript:acalogPopup('/mime/download.?catoid=24&ftype=3&foid=', 'view_flashpoint', 770, 530, 'yes')"})

    return course_data  # parent element of course data


# parses course attributes for easier handling in the degree planner
def get_course_info(course_list):
    parsed_course_list = []  # list of dictionaries

    for course in course_list:
        course_title = course.parent.h3.text.strip()
        course_id = course_title.split(" - ")[0].strip()
        course_subject = course_id.split(" ")[0].strip()
        course_number = course_id.split(" ")[1].strip()
        course_name = course_title.split(" - ")[1].strip()

        # Order from top to bottom on catalog: Description, Prerequsites/Corequisites, When Offered, Cross Listed, Credit Hours
        course_description = course.parent.text.replace(course_title, "").strip()
        course_is_ci = False
        course_credit_hours = "Unknown"
        course_crosslisted = "Not Crosslisted"
        course_offered = "Unknown"
        course_requisites = "None"
        # course_prerequisites = []
        # course_corequisites = []

        if course_description.find("Contact, Lecture or Lab Hours: ") != -1:
            course_description = course_description.split("Contact, Lecture or Lab Hours: ")[0].strip()

        if course_description.find("Credit Hours: ") != -1:
            course_credit_hours = course_description.split("Credit Hours: ")[1].strip()
        course_description = course_description.split("Credit Hours: ")[0].strip()

        if course_description.find("Cross Listed: ") != -1:
            course_crosslisted = course_description.split("Cross Listed: ")[1].strip()
        course_description = course_description.split("Cross Listed: ")[0].strip()

        if course_description.find("When Offered: ") != -1:
            course_offered = course_description.split("When Offered: ")[1].strip()
        course_description = course_description.split("When Offered: ")[0].strip()

        if course_description.find("Prerequisites/Corequisites: ") != -1:
            course_requisites = course_description.split("Prerequisites/Corequisites: ")[1].strip()
        course_description = course_description.split("Prerequisites/Corequisites: ")[0].strip()

        if course_description.find("This is a communication-intensive course.") != -1:
            course_is_ci = True
            course_description = course_description.replace("This is a communication-intensive course.", "").strip()

        print("-------------------------------------------------------")
        print(f"Course Subject: {course_subject}")
        print(f"Course Number: {course_number}")
        print(f"Course Name: {course_name}")
        print(f"Description: {course_description}")
        print(f"Course is communication-intensive: {course_is_ci}")
        print(f"Course Prerequisites/Corequisites: {course_requisites}")
        print(f"Course Offered: {course_offered}")
        print(f"Course Crosslisted: {course_crosslisted}")
        print(f"Credit Hours: {course_credit_hours}")

        parsed_course = {
            "course_subject": course_subject,
            "course_number": course_number,
            "course_name": course_name,
            "course_description": course_description,
            "course_is_ci": course_is_ci,
            "course_requisites": course_requisites,
            "course_offered": course_offered,
            "course_crosslisted": course_crosslisted,
            "course_credit_hours": course_credit_hours
        }
        parsed_course_list.append(parsed_course)

    return parsed_course_list


# main function to generate all pages to be searched
if __name__ == "__main__":
    start_time = time.time()
    courses = []  # list of dictionaries

    # link to website with all courses, last updated Fall 2022
    # http://catalog.rpi.edu/content.php?filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bcourse_type%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=24&expand=1&navoid=606&print=1&filter%5Bexact_match%5D=1#acalog_template_course_filter
    subject_code = "-1"  # -1 searches for all courses, can be replaced with "CSCI" for example to specify subject
    print("Starting Catalog Scraping")
    for page_number in range(1, 21):  # there are 20 pages in the course catalog for 2022-2023
        print(f"Scraping Page {page_number}")
        page_url = f"http://catalog.rpi.edu/content.php?" \
                   f"filter%5B27%5D={subject_code}" \
                   f"&filter%5B29%5D=&filter%5Bcourse_type%5D=" \
                   f"&filter%5Bkeyword%5D=" \
                   f"&filter%5B32%5D=1&filter%5Bcpage%5D={page_number}" \
                   f"&cur_cat_oid=24&expand=1&navoid=606&print=1&filter%5Bexact_match%5D=1#acalog_template_course_filter"

        courses.extend(get_course_info(soup_search(page_url)))  # adds list items to end of list

    print("End Catalog Scraping")

    print("Start writing to JSON File")
    json_object = json.dumps(courses, indent=2)
    with open("catalog_results.json", "w") as outfile:  # write to file
        outfile.write(json_object)
    print("End writing to JSON File")

    # time to run program
    print("--- %s seconds ---" % (time.time() - start_time))
