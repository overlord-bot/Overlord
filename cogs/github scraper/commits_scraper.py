# GitHub commits scraper
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from discord.ext import commands

repo_url = "https://github.com/overlord-bot/Overlord/commits?author=whitefieldcat"

search_data = requests.get(repo_url)
search_soup = BeautifulSoup(search_data.text, 'html.parser')

links = search_soup.find_all("a", {"class": "Link--primary text-bold js-navigation-open markdown-title"}, href=True)

links_list = []
for link in links:
    full_link = "https://github.com" + link['href']
    if full_link not in links_list:
        links_list.append(full_link)

# the buttons at the bottom of the page that say "Newer" and "Older"
page_buttons = search_soup.find_all("div", {"class": "BtnGroup", "data-test-selector": "pagination"})
pprint(next)


