
# from os import name
# classnames=[]
# with open("Studentinfo.json","r+") as f:
#     data = json.load(f)
#     update=data['studentinfo']
#     for p in data['studentinfo']:
#         print('Name: ' + p['name'])
#         print('rollno: ' + str(p['rollno']))
#         classnames.append(p['name'])
#     y={"name": "amit",
#     "rollno": 5}
#     update.append(y)
#     json.dump(data,f)
# print(data)


# Python program to update 
# # JSON 
  
  
# import json 
  
  
# # function to add to JSON 
# def write_json(data, filename='Studentinfo.json'): 
#     with open(filename,'w') as f: 
#         json.dump(data, f, indent=4) 
      
      
# with open('Studentinfo.json') as json_file: 
#     data = json.load(json_file) 
      
#     temp = data['studentinfo'] 
  
#     # python object to be appended 
#     y = {"name":'kshitij', 
#          "rollno": 7
#         } 
  
  
#     # appending data to emp_details  
#     temp.append(y) 

# write_json(data)

import csv
updated=['4','abc','21:19:12','03/24/2021']
rows=[]
fields=[]
with open("Attendance.csv",'r+') as f:
    attendancereader = csv.reader(f)
    fields=next(attendancereader)
    for row in attendancereader:
        rows.append(row)
        rows.append(updated)
print(rows)