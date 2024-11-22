import lxml
import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

msg="kl raghul"

#batting career summay
column_=[]
col=[]

source = requests.get(f"https://www.google.com/search?q={msg}%20cricbuzz").text

page = BeautifulSoup(source, "lxml")
page = page.find("div",class_="kCrYT")

link = page.find("a", href=re.compile(r"[/]([a-z]|[A-Z])\w+")).attrs["href"]
link=link[7:]

page_1=source = requests.get(link).text
page_ = BeautifulSoup(page_1, "lxml")

#playerprofile class
de = page_.find("div",attrs={'id':"playerProfile"})

#name and country
name=de.find('div',attrs={'class':'cb-col cb-col-80 cb-player-name-wrap'})
for i in name:
    print(i.text)

#personal information
personal=de.find('div',attrs={'class':'cb-hm-rght'})

personal_info={}
#teams
d=personal.find_all('div',attrs={'class':"cb-col cb-col-60 cb-lst-itm-sm"})
e=personal.find_all('div',attrs={'class':"cb-col cb-col-40 text-bold cb-lst-itm-sm"})

for i,j in zip(e,d):
    personal_info[i.text]=j.text
print(personal_info)

batting={}
bowling={}

#icc ranking batting
k=personal.find_all('div',attrs={'class':"cb-col cb-col-25 text-right cb-plyr-rank"})
f=personal.find_all('div',attrs={'class':"cb-col cb-col-25 cb-plyr-rank text-right"})

for i,j in zip(k,f[:3]):
    batting[i.text]=j.text
print("batting",batting)

#icc ranking batting
for  i,j in zip(k,f[3:]):
    bowling[i.text]=j.text
print("bowling",bowling)


#profile summary
deta=de.find("div",attrs={'class':'cb-col cb-col-67 cb-bg-white cb-plyr-rt-col'})

#short summary
det=deta.find_all('div',attrs={'class':'cb-plyr-tbl'})

#batting average
for roe in det:
    career=roe.find_all('table',attrs={'class':'table cb-col-100 cb-plyr-thead'})
    for jk in career:
        col.clear()
        column_.clear()
        column=jk.find('tr',attrs={'class':'cb-bg-grey cb-font-12'})
        file_name=roe.find('div',attrs={'class':'cb-font-16 text-bold cb-lst-dom'}).text
        for i in column:
            column_.append(i.text)
        for i in column_:
            if i.strip():
                col.append(i)
        col.insert(0," ")
        
        #print(col)
        df=pd.DataFrame(columns=col)
        rows = []
        # Accumulate rows here

        # Process rows
        row = roe.find('tbody')
        for i in row.find_all('tr'):
            k = i.find_all('td')
            #print(k)
            if len(k) >= len(col):  # Ensure the row matches the column length
                row_data = {col[idx]: k[idx].text.strip() for idx in range(len(col))}
                rows.append(row_data)
        df = pd.DataFrame(rows, columns=col)
        df.to_csv(f"{file_name}.csv", index=False)
        print(f"Saved {file_name}.csv")

#career information
career_info={}
info=deta.find('div',attrs={'class':'cb-col cb-col-100'})
detail_info=deta.find_all('div',attrs={'class':'cb-col cb-col-16 text-bold cb-ftr-lst'})
detail=info.find_all('div',attrs={'class':'cb-col cb-col-84 cb-ftr-lst'})
for i,j in zip(detail_info,detail):
    career_info[i.text]=j.text
print(career_info)



#profile info
profile_info=()
profile=deta.find('div',attrs={'class':'cb-col cb-col-100 cb-player-bio'})
profile_info=profile_info+(profile.text,)
print(profile_info)
