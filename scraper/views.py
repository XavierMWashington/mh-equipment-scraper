from email.quoprimime import body_check
from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json

# Create your views here.
def greet(request):
    return HttpResponse('Hello, user')

def fetchProxy():
    response = requests.get("https://free-proxy-list.net")
    content = BeautifulSoup(response.text, "lxml")
    table = content.find('table')
    rows = table.find_all('tr')

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


def scrapeArmor(request, slug):

    proxies = fetchProxy()
    uaheaders = {
        'User-Agent': 'Mozilla/5.0',
    }

    session = requests.Session()
    result = ""
    url = ""
    
    rank = slug[0:2]
    if(rank == "lr"):
        rankNum = 1
    elif(rank == "hr"):
        rankNum = 0

    slug = slug[3:]
    
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

    tableBody = soup.find_all("tbody")

    armor = []
    skills = []
    images = []

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
            
            armor.append(
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
    jsonedArmor = json.dumps(armor)
    parse = json.loads(jsonedArmor)
    formattedJson = json.dumps(parse, indent=4)

    return HttpResponse(formattedJson)

    #Scraping weapons
    weaponsShortCat = ['gs', 'ls', 'sns', 'db', 'h', 'hh', 'l', 'gl', 'sa', 'cb', 'ig', 'lbg', 'hbg', 'b']
    weaponsSlugs = ["Great+Swords", "Long+Swords", "Sword+&+Shields", "Dual+Blades+List", "Hammers", "Hunting+Horns", "Lances", "Gunlances", "Switch+Axes", "Charge+Blades", "Insect+Glaives", "Light+Bowguns", "Heavy+Bowguns", "Bows"]
    
    #General weapon table data location values
    nameScraper = 0
    attackScraper = 1
    eleAtkScraper = 2
    AffinityScraper = 3
    defenseBonusScraper = 4
    rarityScraper = 5
    rampageSkillsScraper = 6

    for proxy in proxies:
        session.proxies = {"http":proxy, "https": proxy}
        session.trust_env = False

        if(slug == "hh"):
            rarityScraper = 6
            rampageSkillsScraper = 7

        for i in range (0, len(weaponsShortCat)):
            if(slug == weaponsShortCat[i]):
                slug = weaponsSlugs[i]

        url = "https://monsterhunterrise.wiki.fextralife.com/" + slug 
        
        try:
            result = requests.get(url, headers=uaheaders, proxies={"http" : proxy}, timeout=5)
            break
        except:
            pass
    

    try:
        soup = BeautifulSoup(result.text, "html.parser")
    except:
        return HttpResponse("Error: None of the supplied proxies works")

    tableBody = soup.find("tbody")

    #Weapon values
    weapons = []
    images = []
    rampageSkills = []

    #Special Weapon Values
    melodies = None
    shelling = None
    phialType = None
    kinsectLevel = None
    bowgunData = None
    bowData = None

    iter = 0

    for row in tableBody:
        if(row == "\n"):
            continue

        imgData = row.find_all("td")[0].find_all("img")
        for data in imgData:
            slot = ""
            for i in range (1, 4):
                if("level " + str(i) in str(data["alt"])):
                    slot = "Gem lv " + str(i)
                    break
            images.append(slot)

        if(slug == "Hunting+Horns"):
            rarityScraper=6
            rampageSkillsScraper = 7
            melodyData = row.find_all("td")[5].find_all(text=True)
            melodies = []
            for data in melodyData:
                melodies.append(data.text.strip())

        elif(slug == "Gunlances"):
            rarityScraper = 7
            rampageSkillsScraper = 8
            shelling = [row.find_all("td")[5].text, row.find_all("td")[6].text]

        elif(slug == "Switch+Axes" or slug == "Charge+Blades"):
            defenseBonusScraper = 5
            rarityScraper = 6
            rampageSkillsScraper = 7
            phialType = row.find_all("td")[4].text
            splitPoint = 0
            for i in range(0, len(phialType)):
                if(phialType[i] == "l"):
                    splitPoint = i
            #lHalf = saPhialType[0:splitPoint + 1]
            rHalf = phialType[splitPoint + 1:]
            if(rHalf != ""):
                phialType = rHalf
            #saPhialType = lHalf + " " + rHalf

        elif(slug == "Insect+Glaives"):
            defenseBonusScraper = 5
            rarityScraper = 6
            rampageSkillsScraper = 7
            kinsectLevel = row.find_all("td")[4].text

        elif("Bowgun" in slug):
            defenseBonusScraper = 8
            rarityScraper = 9
            rampageSkillsScraper = 10
            deviation = row.find_all("td")[3].text
            recoil = row.find_all("td")[4].text
            bgReload = row.find_all("td")[5].text
            clusterBombType = row.find_all("td")[6].text
            specialAmmoType = row.find_all("td")[7].text
            bowgunData = {"Deviation" : deviation, "Recoil" : recoil, "Reload Speed" : bgReload, "Cluster Bomb Type" : clusterBombType, "Special Ammo Type" : specialAmmoType}

        elif(slug == "Bows"):
            defenseBonusScraper = 9
            rarityScraper = 10
            rampageSkillsScraper = 11
            archShot = row.find_all("td")[4].text
            chargeShot1 = row.find_all("td")[5].text
            chargeShot2 = row.find_all("td")[6].text
            chargeShot3 = row.find_all("td")[7].text
            chargeShot4 = row.find_all("td")[8].text
            coatings = []
            coatingData = row.find_all("td")[12].text
            cutoff = 0
            for i in range(0, len(coatingData)):
                try:
                    if (coatingData[i] == "g" and coatingData[i - 2] == "i"):
                        coatings.append(coatingData[cutoff:i + 1])
                        cutoff = i + 1
                except:
                    pass


            bowData = {"Arc Shot":archShot, "Charge Shot 1": chargeShot1, \
                "Charge Shot 2": chargeShot2, "Charge Shot 3": chargeShot3, \
                    "Charge Shot 4": chargeShot4, "Coatings": coatings}         

        rampageSkillsData = row.find_all("td")[rampageSkillsScraper].find_all("li")
        for data in rampageSkillsData:
            rampageSkills.append(data.text)

        while "" in rampageSkills:
            rampageSkills.remove("")

        weapons.append(
        {"Name" : row.find_all("td")[nameScraper].find("a").text, \
            "Gems": images, \
                "Attack": row.find_all("td")[attackScraper].text, \
                    "Elemental Attack": row.find_all("td")[eleAtkScraper].text, \
                    "Affinity": row.find_all("td")[AffinityScraper].text, \
                    "Defense Bonus": row.find_all("td")[defenseBonusScraper].text, \
                    "Rarity": row.find_all("td")[rarityScraper].text[-1], \
                    "Rampage Skills": rampageSkills})

        if(melodies != None):
            weapons[iter].update({"Melodies ":melodies})

        if(shelling != None):
            weapons[iter].update({"Shelling Type": shelling[0], "Shelling Level": shelling[1]})
        
        if(phialType != None):
            weapons[iter].update({"Phial Type:" : phialType})

        if(kinsectLevel != None):
            weapons[iter].update({"Kinsect Level": kinsectLevel})

        if(bowgunData != None):
            weapons[iter].update(bowgunData)

        if(bowData != None):
            weapons[iter].update(bowData)

        images = []
        rampageSkills = []

        melodies = None
        shelling = None
        phialType = None
        kinsectLevel = None
        bowgunData = None
        bowData = None

        iter+= 1


    jsonedWeapons = json.dumps(weapons)
    parse = json.loads(jsonedWeapons)
    formattedJson = json.dumps(parse, indent=4)

    return HttpResponse(formattedJson)
