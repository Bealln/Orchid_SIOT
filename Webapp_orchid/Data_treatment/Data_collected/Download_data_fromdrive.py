import csv
import gspread, oauth2client
from oauth2client.service_account import ServiceAccountCredentials
import json


JSON_FILENAME = 'data.json'
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Weather_data").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
list_of_values = sheet.get_all_values()
#titles = sheet.cell(2,1).value
#print(list_of_hashes)
#print(list_of_values)

#printone row. I need to loop this so I get values for ALL the rows!!!
#length = len(list_of_values)

i = 1

#print(values_list)
#len(list_of_values)


while i < len(list_of_values):
    values_list = sheet.row_values(i)
    with open('test.csv', 'w', newline='') as f:
        headers = ["Date", "Time", "Measurement", "Presence"]
        w = csv.DictWriter(f, fieldnames=headers)
        writer = csv.writer(f)
        writer.writerow(values_list)
    i = +1





