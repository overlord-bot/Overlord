# GitHub commits, currently only finds a user's commits in the main branch of a GitHub Repository
import requests
from bs4 import BeautifulSoup


def find_links(url):
    print("Searching: " + url)
    search_data = requests.get(url)
    search_soup = BeautifulSoup(search_data.text, 'html.parser')

    # finds all the commit links on the page
    links = search_soup.find_all("a", {"class": "Link--primary text-bold js-navigation-open markdown-title"}, href=True)

    # adds links into links_list if they are not already in it
    for link in links:
        full_link = "https://github.com" + link['href']
        if full_link not in links_list:
            links_list.append(full_link)

    # the buttons at the bottom of the page that say "Newer" and "Older"
    page_buttons = search_soup.find_all("a", {"rel": "nofollow", "class": "btn btn-outline BtnGroup-item"})

    has_more_pages = False
    for button in page_buttons:
        if button.get_text() == "Older":
            has_more_pages = True
            find_links(button['href'])


if __name__ == "__main__":
    links_list = []  # list of commits in the main branch

    repo_url = "https://github.com/overlord-bot/Overlord/commits?author=jwgit9"

    find_links(repo_url)
    for link in links_list:
        print(link)
    print(len(links_list))
