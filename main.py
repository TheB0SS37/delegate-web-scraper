# Developed by Ian Wagner
# This program collects information on current MGA Delegates and Senators

from bs4 import BeautifulSoup
import requests
import re
import csv


# function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)

    # response will be provided in JSON format
    return response.text


# assign required credentials
# assign URL

def createMemberLinks(url):
    # create document
    html_document = getHTMLdocument(url)

    # create soup object
    soup = BeautifulSoup(html_document, 'html.parser')
    links_to_members = []
    # find all the anchor tags with "href"
    # attribute starting with "https://"
    for link in soup.find_all('a', attrs={'href': re.compile("^/mgawebsite/Members/Details/")}):
        # display the actual urls
        links_to_members.append("https://mgaleg.maryland.gov" + link.get('href'))
    return links_to_members


# Scrapes every member page in the links list
def scrapeMembers(links):
    print("Gathering members...\n")
    members = [["Name", "Room", "Phone #"]]

    for i in range(0, len(links), 2):
        url_to_scrape = links[i]

        html_document = requests.get(url_to_scrape)
        soup = BeautifulSoup(html_document.content, 'html.parser')
        name = formatName(str(soup.find('h2').contents[0].string)) # name
        table = soup.find('dl', attrs={'class': 'row'}).contents[15]
        room = table.find('dd').contents[0].strip()  # room
        phone = table.find('dl').contents[3].contents[0].strip()  # phone
        # Check for duplicates, this could be faster
        if [name, room, phone[6:18]] not in members:
            members.append([name, room, phone[6:18]])
        print(len(members))
    return members
def formatName(name):
    new_name = name.split()
    first_name = ''
    last_name = ''
    removables = ["Jr.", "Sr.", "II", "III", "IV"] # add extra name items to be removed
    if "Senator" in new_name:
        new_name.remove("Senator")
    elif "Delegate" in new_name:
        new_name.remove("Delegate")
    for r in removables:
        if r in new_name:
            new_name.remove(r)


    if 'Jr.' in new_name:
        new_name.remove('Jr.')
    if 'Sr.' in new_name:
        new_name.remove('Sr.')

    # remove commas
    i = 0
    for i in range(len(new_name)):
        if ',' in new_name[i]:
            print(f'removing comma from {new_name[i]}')
            new_name[i] = new_name[i][:-1]

    # Handle first names
    i = 0
    if len(new_name) > 0 and '.' in new_name[0]: # If first name is just initials, handle that
        print(f'period as first name {new_name[0]}')
        while i < len(new_name) and '.' in new_name[i]:
            print(f'Im running on {new_name[i]}')
            first_name += new_name[i]
            i += 1
    elif len(new_name) > 0: # Complete first name, grab first name
        first_name = new_name[0]

    # Handle last name, remove any initials.
    while len(new_name) > 0:
        if '.' in new_name[0]:
            new_name.pop(0)
        else:
            last_name = new_name.pop(0)

    return last_name + ', ' + first_name

def createCSV(members):
    with open('testsenators.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(members)
    file.close()

def chooseMembers():
    base_link = "https://mgaleg.maryland.gov/mgawebsite/Members/Index/"
    directory = ["house", "senate"]
    while True:
        choice = input("Press 1 then enter for House members, 2 then enter for Senate members ")
        if choice == "1":
            return base_link + directory[0]
        elif choice == "2":
            return base_link + directory[1]


def printMembers(members):
    for member in members:
        print(member)


def main():
    url_to_scrape = chooseMembers()
    membersInfo = scrapeMembers(createMemberLinks(url_to_scrape))
    createCSV(membersInfo)
    printMembers(membersInfo)


if __name__ == "__main__":
    main()
