from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
import os


# Create your views here.
def greet(request):
    return HttpResponse('Hello, user')

def fetchProxy():
    response = requests.get("https://free-proxy-list.net")
    content = BeautifulSoup(response.text, "lxml")
    table = content.find('table')
    rows = table.find_all('tr')
    cols = [[col.text for col in row.find_all('td')] for row in rows]

    proxies = []

    for row in rows:
        try:
            dataRow = row.find_all('td')
            if(dataRow[4].text == "elite proxy" and dataRow[6].text == "yes"):
                proxies.append("https://" + dataRow[0].text + ":" + dataRow[1].text)
        except:
            pass


    #print(proxies)
    return proxies


def scrapeData(request, slug):

    rankNum = int(slug[0])

    slug = slug[2:]

    print(rankNum)
    print(slug)

    proxies = fetchProxy()
    uaheaders = {
        'User-Agent': 'Mozilla/5.0',
    }

    session = requests.Session()
    
    for proxy in proxies:
        print(proxy)
        session.proxies = {"http":proxy, "https": proxy}
        session.trust_env = False

        url = "https://monsterhunterrise.wiki.fextralife.com/" + slug + "+Armor"
  
        try:
            result = requests.get(url, headers=uaheaders, proxies={"http" : proxy}, timeout=5)
            break
        except:
            pass
    

    try:
        soup = BeautifulSoup(result.text, "html.parser")
    except:
        return HttpResponse("Error: None of the supplied proxies works")

    #print(soup)

    tableBody = soup.find_all("tbody")

    names = []
    skills = []
    images = []

    iter = 0

    for row in tableBody[rankNum]:
        try:
            skillData = row.find_all("td")[1].find_all("a")
            imgData = row.find_all("td")[2].find_all("img")
            
            for data in skillData:
                skills.append(data.text)

            while "" in skills:
                skills.remove("")

            for data in imgData:
                slot = ""
                for i in range (1, 4):
                    if("level " + str(i) in str(data["alt"])):
                        slot = "Gem Lv " + str(i)
                        break
                
                images.append(slot)
            
            names.append(
                {"Name" : row.find_all("td")[0].text, \
                    "Skills" : skills, \
                    "Gem Slots" : images, \
                    "Rarity:" : row.find_all("td")[3].text, \
                        "Defense": row.find_all("td")[4].text, \
                            "Fire Resist": row.find_all("td")[5].text, \
                            "Water Resist": row.find_all("td")[6].text, \
                            "Thunder Resist": row.find_all("td")[7].text, \
                            "Ice Resist" : row.find_all("td")[8].text, \
                            "Dragon Resist" : row.find_all("td")[9].text})

            skills = []
            images = []
        except:
            continue

    #print(names)
    jsonedNames = json.dumps(names)
    parse = json.loads(jsonedNames)
    formattedJson = json.dumps(parse, indent=4)

    return HttpResponse(formattedJson)

