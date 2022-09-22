# RPI Catalog Scraper
import requests
from bs4 import BeautifulSoup

from discord.ext import commands

# subject_codes = ["-1", "CSCI"] # add remaining codes later
subject_code = "CSCI"
url = f"http://catalog.rpi.edu/content.php?" \
      f"filter%5B27%5D={subject_code}" \
      f"&filter%5B29%5D=" \
      f"&filter%5Bcourse_type%5D=" \
      f"&filter%5Bkeyword%5D=" \
      f"&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=24&expand=1&navoid=606&print=1&filter%5Bexact_match%5D=1#acalog_template_course_filter"
print(url)


search_data = requests.get(url)
search_soup = BeautifulSoup(search_data.text, 'html.parser')


