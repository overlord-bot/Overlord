from tabulate import tabulate 

table = [[1, "CSCI 1100", "MATH 1010" , "PHYS 1100", "HASS Core Elective"],
         [2, "BIOL 1010", "BIOL 1015" , "CSCI 1200", "MATH 1020"],
         [3, "Mathematics Option I", "HASS Core Elective", "CSCI 2200" , "CSCI 2500"],
         [4, "Mathematics Option II", "HASS Core Elective", "CSCI 2300", "CSCI 2600"],
         [5, "CS Capstone", "HASS Core Elective", "Free Elective", "CSCI 4210"],
         [6, "Science Option", "HASS Core Elective", "Free Elective", "CSCI 4430"],
         [7, "CS Capstone", "Free Elective", "Free Elective", "CSCI 4430"],
         [8, "CS Capstone", "Free Elective", "Free Elective", "Free Elective"]
]
table1 = [[1,2,3,4],
          ["CSCI 1100","BIOL 1010","Mathematics Option I","Mathematics Option II"],
          ["MATH 1010","BIOL 1015","HASS Core Elective","HASS Core Elective"],
          ["PHYS 1100","CSCI 1200", "CSCI 2200","CSCI 2300"],
          ["HASS Core Elective","MATH 1020","CSCI 2500","CSCI 2600"]]

firstsem = [[1],["CSCI 1100"], ["MATH 1010"] , ["PHYS 1100"], ["HASS Core Elective"]]
secondsem = [[2],["BIOL 1010"], ["BIOL 1015"] , ["CSCI 1200"], ["MATH 1020"]]

'''
firstsemtable = tabulate (firstsem,tablefmt = 'html')
print (firstsemtable)

secondsemtable =  tabulate (secondsem,tablefmt = 'html')
print (secondsemtable)

'''
tableformat = "<style> table,th, td {border: 1px solid black; width: 200px;margin-left:auto;margin-right:auto;}table {text-align: center;} </style>"
print (tableformat)

def printtable (schedulelist):
    htmlschedule = tabulate(schedulelist,tablefmt = 'html')
    print (htmlschedule)


printtable (firstsem)
printtable (secondsem)

'''
htmltable = tabulate (table1,tablefmt = 'html')
print (htmltable)
'''
'''
file_html = open ("degree.html","w")
file_html.write(tabulate (table,tablefmt = 'html'))
file_html.close()
''' 