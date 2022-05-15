import requests
from bs4 import BeautifulSoup
import ReadCaptchaText #file for capcha decode
import mainpagedata #file for geting data table

BASE_URL="https://drt.gov.in/front/page1_advocate.php"
r = requests.get(BASE_URL)
soup = BeautifulSoup(r.content, 'html.parser')
schemanamevalue=[]
for option in soup.find_all('option'):# geting dropdown value
    try:
        schemanamevalue.append(option["value"])
    except:
        pass

for schemaname in schemanamevalue:
    try:
        s = requests.Session()
        file = open("myfile.Png", "wb")
        html = s.get("https://drt.gov.in/front/captcha.php")
        file.write(html.content)
        file.close()
        answer=ReadCaptchaText.captcha_code()  # finding the capcha value
        data = {"answer": answer, "name": "sha", "schemaname": schemaname}
        r = s.post(BASE_URL, data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        mainpagedata.mainpagedatafunction(soup) # passing to function  for saving data to database 
        print ("data save whose schemanamevalue is: " , schemaname)
    except:
        pass
    s.close()
