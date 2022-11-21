import requests
from bs4 import BeautifulSoup
import json

page = requests.get("http://catalog.rpi.edu/preview_program.php?catoid=24&poid=6389&returnto=604") #http://catalog.rpi.edu/preview_program.php?catoid=24&poid=6545&returnto=604

if page.status_code == 200: 
    print("Successfully downloaded page")
else: 
    print("Error downloading page")


soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify)

#Seperates div into children
def getInfoFromDiv(div):
    classes = []
    ul_children = div.findChildren("ul" , recursive=False) 
    if(len(ul_children) >= 1): 
        li_children = ul_children[0].findChildren("li" , recursive=False) 
        classes = getInfoFromChildren(li_children)
    if(len(ul_children) >= 2): #some have secondary section
        second_li_children = ul_children[1].find_all('span')
        classes += getInfoFromChildren(second_li_children)
    return classes



#convert to text
def getInfoFromChildren(children):
    classes = []
    for child in children:
        #split = child.text.split('Credit Hours: ')
        class_name = child.text.replace("\xa0", " ") #.replace removes \xa0 (hidden character)
        classes.append(class_name)
        #print(class_name)
    return classes

def getRefs(): #Get links to every major
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
        major = a_major.text
        refs.append([major, a_major["href"]])
    return refs

def getPastCreditHours(list, name): #Get how many credit hours already needed
    for item in list:
        if(item['name'] == name):
            #print(item)
            info = int(item['credits']), int(item['number_classes'])
            #print(info)
            return info
    return 0, 0

def itemIndex(list, name): #Find index of item in list
    for i in range(len(list)):
        item = list[i]
        if(item["name"] == name):
            return i
    return -1
        

def isElective(text): #Checks to see if course is elective based on key words
    text = text.lower()
    elective_key_words = ["elective", "option", "cas course", "sts course", "hass approved inquiry and communication intensive course", "concentration", "capstone", "approved project", "area of study", "4000-level comm course", "biology requirement", "track course"]
    return any(substring in text for substring in elective_key_words)

def write_to_dict(classes):
    dict_list = []
    name = "undefined"

    for course in classes:
        course_dict = {}

        #Check if elective
        if isElective(course):
            elective_split = course.split("Credit Hours: ")
            name = elective_split[0].strip() \
                   .split("\n\t")[0] #removes extra line

            credit_hours, num_classes = getPastCreditHours(dict_list, name)
            num_classes += 1

            if len(elective_split) >= 2:
                if len(elective_split[1]) >= 1:
                    try:
                        credit_hours += int(elective_split[1].strip()[0]) #Get second part of split, remove spaces, take first number
                    except:
                        print("Error formatting credit hours for {}. Starting value *{}* and trying to add *{}*".format(name, credit_hours, elective_split[1][0]))
    
            course_dict = {
                "name": name,
                "type": "elective",
                "credits": credit_hours,
                "number_classes": num_classes
            }
        else: #If anything else 
            credit_hours_split = course.split("Credit Hours: ")

            #Find credit hours
            credit_hours = -1
            if len(credit_hours_split) >= 2:
                if len(credit_hours_split[1]) > 0:
                    credit_hours = int(credit_hours_split[1][0])

            #Find name and ID
            tag = "none"
            number = -1
            name_split = credit_hours_split[0].split(" - ")
            if len(name_split) >= 2: #If length is 2+ then tag and number exist
                name = name_split[1]

                if name.lower().count('footnote') != 0 or name.lower().count('or') != 0: #Special case for footnote
                    continue

                tag_split = name_split[0].split(" ")
                if len(tag_split) >= 2:
                    tag = tag_split[0]
                    number = tag_split[1]

                    try:
                        number = int(number)
                    except ValueError:
                        try:
                            number = int(number.replace("XXX", "000"))
                        except ValueError:
                            pass
            else:
                name = name_split[0].strip()
                if name.lower().count('footnote') != 0 or name.lower().count('or') != 0: #Special case for footnote
                    continue
        
            course_dict = {
                "name": name,
                "type": "course",
                "credits": credit_hours,
                "major": tag,
                "course_id": number
            }
        index = itemIndex(dict_list, name)
        if index != -1:
            dict_list.pop(index)
        dict_list.append(course_dict)

    return dict_list

dict = {}
for ref_tup in getRefs():
    major = ref_tup[0]
    ref = ref_tup[1]
    page = requests.get("http://catalog.rpi.edu/" + ref)
    #page = requests.get("http://catalog.rpi.edu/preview_program.php?catoid=18&poid=4016&returnto=439") 

    if page.status_code != 200: 
        print("Error downloading ref:", ref)
        continue

    soup = BeautifulSoup(page.content, 'html.parser')

    years = soup.find_all('div', class_="custom_leftpad_20")
    classes = []
    for year in years[1:]: #Skipping first entry as is description of major
        for semester in year.children:
            classes += getInfoFromDiv(semester)
    dict[major.strip()] = write_to_dict(classes)
    #break

json_object = json.dumps(dict, indent=2)
with open("class_results.json", "w") as outfile:  # write to file
    outfile.write(json_object)

