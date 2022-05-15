import sqlite3
import os
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
import pandas as pd

url="https://drt.gov.in/drtlive/Misdetailreport.php?no="


def removespace(string):
    string=string.replace(' ', '')
    string=string.replace('\xa0', '')
    string=string.replace('\r\n\r\n\r', '')
    string=string.replace('\r\n\r', '')
    string=string.replace('\r\\r', '')
    string=string.replace('\t\\t', '')
    string=string.replace('\n\\n', '')
    string=string.replace('\n\r', '')
    string=string.replace('\t', '')      
    string=string.strip()
    return string

def alllink(*arg):
    links=arg
    # print(sendlinks)
    for sendlinks in links:
        for sendlink in sendlinks:
            print(sendlink)
            try:
                r = requests.get(url+sendlink)
                soup = BeautifulSoup(r.content, 'html.parser')
                table=soup.find("table")
                dict={}
                temp=""
                for  count ,value in enumerate  (table.find_all("td")):
                    if count<10:
                        if count==0 or count%2==0:
                            temp=removespace(value.text)
                        else:
                            dict[temp]=removespace(value.text)
                    if count>10 and count<14:
                        if count==0 or count%2==0:
                            dict[temp]=removespace(value.text)        
                        else:
                            temp=removespace(value.text)
                    if count==15:
                        dict["PETITIONER/APPLICANT DETAIL"]=removespace(value.text)
                    if count==16:
                        dict["RESPONDENTS/DEFENDENT DETAILS"]=removespace(value.text)
                        break
                df=pd.DataFrame([dict])
                df["View More"]=sendlink
                try:
                    df1=pd.read_csv("savefile.csv")
                    df3 = df1.append(df, ignore_index=True)
                    df3.to_csv("savefile.csv",index=False)
                except:
                    df.to_csv("savefile.csv",index=False)
                newdata=[]
                dict={"Court  Name":[],'Causelist Date':[],'Purpose':[]}
                for  count ,value in enumerate(table.find_all("td")):
                    if count>19:
                        finallvalue=removespace(value.text)
                        newdata.append(finallvalue)
                for count,value in enumerate(dict):
                    dict[value]=newdata[count::3]
                maindata=pd.DataFrame.from_dict(dict)
                maindata["View More"]=sendlink        
                disk_engine = create_engine('sqlite:///linktable2.db')
                maindata.to_sql('linktable2', disk_engine, if_exists='append',index=False)
            except:
                pass
    return(True)
   