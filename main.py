# Developed by Ian Wagner
# This program collects information on current MGA Delegates and Senators

from bs4 import BeautifulSoup
import requests
import re


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
    members = []
    for i in range(0, len(links), 2):
        url_to_scrape = links[i]

        html_document = requests.get(url_to_scrape)
        soup = BeautifulSoup(html_document.content, 'html.parser')
        name = soup.find('h2').contents[0]  # name
        table = soup.find('dl', attrs={'class': 'row'}).contents[15]
        room = table.find('dd').contents[0].strip()  # room
        phone = table.find('dl').contents[3].contents[0].strip()  # phone
        members.append(name + " | " + room + " | " + phone[6:18] + '\n')
    return members


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
    printMembers(membersInfo)


if __name__ == "__main__":
    main()
