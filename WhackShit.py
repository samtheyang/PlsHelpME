from bs4 import BeautifulSoup
import pickle
import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter

soup = BeautifulSoup(open("message.html", encoding= 'utf-8'), "lxml")
print('Data imported.')
namelist = []
bodylist = []
timestamplist = []

# Stores all the separate names into a list.
for hit in soup.findAll(attrs={'class': ['_3-96 _2let']}):
    sender = hit.text.strip()
    bodylist.append(sender)
# Stores all the message bodies into a list.
for hit in soup.findAll(attrs={'class': ['_3-96 _2pio _2lek _2lel']}):
    body = hit.text.strip()
    namelist.append(body)
    # for div in soup.find_all("div", {'class': '_tqp'}):
    #     div.decompose()
# Stores all the dates into a list.
for hit in soup.findAll(attrs={'class': ['_3-94 _2lem']}):
    dt = hit.text.strip()
    timestamplist.append(dt)

print('Data stored as list.')

# # dump lists into pickle files
# # pickle.dump(bodylist, open("names.pkl","wb"))
# # pickle.dump(namelist, open("bodies.pkl","wb"))
# # pickle.dump(timestamplist, open("timestamp.pkl","wb"))

# # store pickle files as variables
# name = DataFrame(pd.read_pickle("names.pkl"))
# body = DataFrame(pd.read_pickle("bodies.pkl"))
# time = DataFrame(pd.read_pickle("timestamp.pkl"))

# Store lists into data frame
textdata = {'Name': namelist, 'Body': bodylist, 'Time': timestamplist}
df = DataFrame(textdata)
writer = ExcelWriter('Output.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
print('Stored as data frame.')

# Convert dates into datetime objects
df['datetime'] = pd.to_datetime(df['Time'], infer_datetime_format=True)

# Remove unnecessary messages
search_for = ['The video chat ended', 'missed a video chat', 'sent a photo', 'sent a video', 'sent a sticker']
df = df[~df.Body.str.contains('|'.join(search_for))]

# Removing reactions to messages
for a in (("My_Name", " "), ("Sender_Name", " ")):
    df['Body'] = df['Body'].replace(*a)

# Write to excel file and save
df.to_excel(writer, sheet_name='Sheet1', header=True, encoding='utf-16')
writer.save()
print('Saved.')


