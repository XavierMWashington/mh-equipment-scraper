from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests
import json
import os


# Create your views here.
def greet(request):
    return HttpResponse('Hello, user')

def highRankHelms(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Head+Armor"
    return scrapeData(urlRequest, 0)

def lowRankHelms(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Head+Armor"
    return scrapeData(urlRequest, 1)

def highRankChests(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Chest+Armor"
    return scrapeData(urlRequest, 0)

def lowRankChests(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Chest+Armor"
    return scrapeData(urlRequest, 1)

def highRankArms(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Arms+Armor"
    return scrapeData(urlRequest, 0)

def lowRankArms(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Arms+Armor"
    return scrapeData(urlRequest, 1)

def highRankWaists(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Waist+Armor"
    return scrapeData(urlRequest, 0)

def lowRankWaists(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Waist+Armor"
    return scrapeData(urlRequest, 1)

def highRankLegs(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Legs+Armor"
    return scrapeData(urlRequest, 0) 

def highRankLegs(request):
    urlRequest = "https://monsterhunterrise.wiki.fextralife.com/Legs+Armor"
    return scrapeData(urlRequest, 1)   

def scrapeData(url, rankNum):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    for s in soup.select('script'):
        s.extract()

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