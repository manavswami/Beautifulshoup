from bs4 import BeautifulSoup
import linkpagedata
import sqlite3
import os
from sqlalchemy import create_engine
import pandas as pd

#  remove garbage value 
def removespace(string):
    string=string.replace(' ', '')
    string=string.replace('\xa0', '')
    string=string.replace('\r\n\r\n\r', '')
    string=string.replace('\r\n\r', '')
    string=string.replace('\r\\r', '')
    string=string.replace('\t\\t', '')
    string=string.replace('\n\\n', '')
    string=string.replace('\n\r', '')    
    string=string.strip()
    return string
def mainpagedatafunction(soup):
    try:
        table = soup.findAll('table')[1] # findi table  value
        colums=str(table.find('tr').text).split("\n")[1:-2] # finding column name 
        df = pd.DataFrame(columns=[colums]) 
        dict={}
        table=soup.find_all("table")
        temp=[]
        for  count ,value in enumerate  (table[1].find_all("td")):
            finaltext=removespace(value.text)
            temp.append(finaltext)
        for count,value in enumerate (colums):
            if value not in dict:        
                dict[value]=temp[count::9]
        data = []   
        link=soup.find_all('a')
        allnewlinks=[]
        for i in link:
            if "javascript:popsurety_detailreport" in i.get('href'):  # getting forward links
                k=i.get('href')[i.get('href').find("(")+2:i.get('href').find(")")-1]
                allnewlinks.append(k)
        dict["View More"]=allnewlinks
        linkpagedata.alllink(allnewlinks)
        maindata=pd.DataFrame.from_dict(dict)
        # print(maindata.columns)
        disk_engine = create_engine('sqlite:///maintable.db') #storing in database
        maindata.to_sql('maintable', disk_engine, if_exists='append',index=False)
        df=pd.read_csv("savefile.csv")
        df=df[["Diaryno/Year","CaseType/CaseNo/Year","DRTDetail","DateofFiling.","CaseStatus.","IntheCourtof","PETITIONER/APPLICANT DETAIL","RESPONDENTS/DEFENDENT DETAILS","View More"]]
        disk_engine = create_engine('sqlite:///linktable1.db')
        df.to_sql('linktable1', disk_engine, if_exists='append')
    except:
        pass
    return True