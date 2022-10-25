# Web scraper module for Overlord-Bot
Overview: This module is used to webscrape information from many websites.
Currently, they scrape information from MyAnimeList, GitHub, and an Overlord wiki site.

## Scraper Commands
### GitHub Command
- Returns a text file with a list of the links of all commits a user has made in a given repository. 
  Also counts the number of commits in total.
- To use the command type `!commit_list` followed by the username, repository name, and organization name (if applicable).
- `!commit_list <username> <repository_name> <organization_name (if applicable)>`

### MyAnimeList.net Command
- Returns the link of the page for an anime listed in MyAnimeList.net.
- Currently, the command does not work with titles with 3 or more words.
- To use the command type `!anime` followed by the name of the anime.
- `!anime <title of anime>`

### Overlord Wiki (Fandom) Command
- Returns the link of a page for a character from the anime Overlord listed in the Fandom wiki.
- To use the command type `!overlordfacts` followed by the name of the Overlord character.
- `!overlordfacts <name of Overlord character>`

### Development Plans
- GitHub Scraper: Currently no plans for further development.
- MyAnimeList Scraper: Need to fix a bug preventing search of anime titles longer than 2 words.
- Overlord Wiki Scraper: No plans for further development.
