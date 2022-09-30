import requests
from bs4 import BeautifulSoup

page = requests.get("http://catalog.rpi.edu/preview_program.php?catoid=24&poid=6545&returnto=604")

if page.status_code == 200: 
    print("Successfully downloaded page")
else: 
    print("Error downloading page")


soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify)

#Seperates div into children
def getInfoFromDiv(div):
    ul_children = div.findChildren("ul" , recursive=False) 
    if(len(ul_children) >= 1): 
        li_children = ul_children[0].findChildren("li" , recursive=False) 
        getInfoFromChildren(li_children)
    if(len(ul_children) >= 2): #some have secondary section
        second_li_children = ul_children[1].find_all('span')
        getInfoFromChildren(second_li_children)



#convert to text
def getInfoFromChildren(children):
    for child in children:
        split = child.text.split('Credit Hours: ')
        class_name = split[0].strip() #.strip removes \xa0 (hidden line break character)
        credits = split[1][0]
        print([class_name, credits])

div = soup.find_all('div', class_="acalog-core")
#tons of acalog-core divs, need to find a way which one is the right one to access. Only need "Fall", "Spring" of every year

#div[1] refers to First Year --> Fall
getInfoFromDiv(div[1]) 








