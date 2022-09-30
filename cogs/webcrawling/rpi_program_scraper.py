import requests
from bs4 import BeautifulSoup

page = requests.get("http://catalog.rpi.edu/preview_program.php?catoid=24&poid=6389&returnto=604") #http://catalog.rpi.edu/preview_program.php?catoid=24&poid=6545&returnto=604

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
        print(class_name)

def getRefs():
    program_req = requests.get("http://catalog.rpi.edu/content.php?catoid=24&navoid=604")

    if program_req.status_code == 200: 
        print("Successfully downloaded programs")
    else: 
        print("Error downloading programs")
        return

    program_dir = BeautifulSoup(program_req.content, 'html.parser')
    block = program_dir.find_all('td', class_='block_content', colspan='2')[0]
    program_list = block.find('ul', class_='program-list')

    refs = []
    for li_major in program_list.children:
        a_major = li_major.find('a')
        if a_major == -1:
            continue
        refs.append(a_major["href"])
        major = a_major.text
    return refs

for ref in getRefs():
    page = requests.get("http://catalog.rpi.edu/" + ref) 

    if page.status_code == 200: 
        print("Successfully downloaded ref:", ref)
    else: 
        print("Error downloading ref:", ref)
        continue

    soup = BeautifulSoup(page.content, 'html.parser')

    years = soup.find_all('div', class_="custom_leftpad_20")
    for year in years:
        for semester in year.children:
            getInfoFromDiv(semester)
