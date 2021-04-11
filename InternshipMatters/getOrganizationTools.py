import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

now = datetime.now()
year_start, year_end = 2010, now.year
organizationDict, organizationDict_Fail = {}, {}
json_succcess, json_fail  = {}, {}
resp_encode = 'big5'

def getDetailData(url_detail, name=None ):
    data = {}
    detailPage = f"http://internship.guidance.org.tw/internship_sheet.php{url_detail}"
    soup = getElementsByUrl(detailPage)
    if soup is None:
        return None
    table = soup.find('table', attrs={'id':'table2'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 2:
            continue
        if len(cols) == 2:
            f0 = re.sub(r'(\u3000)|(\xa0)', '', re.sub(r'(\t)|(\n)|(\r)', '', cols[0].text))
            f1 = re.sub(r'(\u3000)|(\xa0)', '', re.sub(r'(\t)|(\n)|(\r)', '', cols[1].text))
            data[f0]  = f1
        elif len(cols) == 3:
            f1 = re.sub(r'(\u3000)|(\xa0)', '', re.sub(r'(\t)|(\n)|(\r)', '', cols[1].text))
            f2 = re.sub(r'(\u3000)|(\xa0)', '', re.sub(r'(\t)|(\n)|(\r)', '', cols[2].text))
            data[f1]  = f2
        
    return data
    #table2 = 實習機構自評表

def getElementsByUrl(url):
    try:
        resp = requests.get(url,headers={"User-Agent": "curl/7.61.0"})
        resp.encoding = resp_encode
        soup = BeautifulSoup(resp.text,"html.parser")
        return soup
    except:
        return None


for year in range(year_start, year_end):
    #print(F'-----{year} Start of Data-----')
    
    pageIndex = 1
    while True:
        #print(F'----- Page {pageIndex} Start-----')
        url = f"http://internship.guidance.org.tw/internship_sheet.php?action=verify_pass&year={year}&sql_study=&pages={pageIndex}"
        soup = getElementsByUrl(url)
        if soup is None:
            json_fail[f"{year}_Page_{pageIndex}"] = e[url]
            break
        elements = soup.select("td.year_6 a")
        if len(elements) <= 0: break # Break if no data, End of this year
        for e in elements:
            #print(F"{s.text}: {s['href']}")
            if e.text not in json_succcess and  e.text not in json_fail :
                #organizationDict[e.text] = e['href']

                #Get Detail
                detail = getDetailData(e['href'], e.text)
                if detail is None:
                    json_fail[e.text] = e['href']
                else:
                    json_succcess[e.text] = detail
        pageIndex += 1
        #print(F'----- Page {pageIndex} End -----')

    #print(F'-----{year} End of Data-----') 

# Output dict
organizationDict['Counts'] = len(json_succcess)
organizationDict['Organization'] = json_succcess

organizationDict_Fail['Counts'] = len(json_fail)
organizationDict_Fail['Organization'] = json_fail

nowStr = now.strftime("%Y_%m_%d_%H%M%S")
with open(f'organizationDict_{nowStr}.txt', 'w', encoding="utf-8") as outfile:
    json.dump(organizationDict, outfile, ensure_ascii=False)

with open(f'organizationDict_Fail_{nowStr}.txt', 'w', encoding="utf-8") as outfile2:
    json.dump(organizationDict_Fail, outfile2, ensure_ascii=False)
    
#print(f"Result: {organizationDict}")
