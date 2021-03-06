import urllib.request, json
import sys
import csv
import requests
from urllib.request import Request, urlopen

DEBUG = 0 #allows to see output of all information
WRITE = 1 #locks/unlocks the ability to write it into .csv files

if len(sys.argv) < 2:
    print("Not enough information given")
    exit()

githubRepo =  str(sys.argv[1])
githubToken = str(sys.argv[2])
issueOrRelease = str(sys.argv[3])

testHeader = {'Authorization': 'token'  + githubToken}

githublink = "https://api.github.com/repos/" + githubRepo

if issueOrRelease == "issue":
    issue = 1
elif issueOrRelease == "release":
    issue = 0
else:
    print("No choice of issue or release given")
    exit()

if DEBUG:
    print(str(issue))

if DEBUG:
    print("concatenated githublink: " + githublink)

with urlopen(Request(githublink, data=None, headers=testHeader, origin_req_host=None, unverifiable=False, method=None)) as url:
    data = json.loads(url.read().decode())

name = data['name']
id = data['node_id']
creationDate = data['created_at']
updateDate = data['updated_at']
numStars = data['stargazers_count']
numWatchers = data['watchers_count']
numForks = data['forks_count']
license = data['license']
hasLicense = True
if license is None:
    hasLicense = False
    licenseName = "None"
else:
    licenseName = data['license']['name']
githubURL = data['url']
pushedDate = data['pushed_at']
numRelease = 0

issueLink = "https://api.github.com/search/issues?q=repo:" + githubRepo + "+type:issue"
if DEBUG:
    print(issueLink)

#get the total number of issues
with urllib.request.urlopen(Request(issueLink, data=None, headers=testHeader, origin_req_host=None, unverifiable=False, method=None)) as url:
    issueData = json.loads(url.read().decode())
numIssues = issueData['total_count']

if DEBUG:
    print("\tname: " + name)
    print("\tnode ID: " + id)
    print("\tcreation date: " + creationDate)
    print("\tupdate date: "  + updateDate)
    print("\tnum stars: " + str(numStars))
    print("\tnum watchers: " + str(numWatchers))
    print("\tnum forks: " + str(numForks))
    print("\tnumber of issues: " + str(numIssues))
    print("\turl: " + githubURL)
    if hasLicense:
        print("\tLisense:" + licenseName)
    print("\tlatest commit: " + pushedDate)

if DEBUG:
    print("Issue number: " + str(issue))
if issue:
    #get issues
    issueLink = "https://api.github.com/repos/" + githubRepo + "/issues?state=all&page=1"
    with urllib.request.urlopen(Request(issueLink, data=None, headers=testHeader, origin_req_host=None, unverifiable=False, method=None)) as url:
        issueData = json.loads(url.read().decode())
    issueBody = []
    issueTitle = []
    dateIssueCreated = []
    issueID = []
    issueAuthor = []
    issueState = []
    issuePageIncrement = 2
    accumulatedIssues = len(issueData)
    print("og accumulated issues:" + str(accumulatedIssues))
    print("new num issues: " + str(numIssues))

    while accumulatedIssues != numIssues:
        i = 0
        while i < len(issueData):
            issueAuthor.append(issueData[i]['user']['login'])
            issueID.append(issueData[i]['node_id'])
            dateIssueCreated.append(issueData[i]['created_at'])
            issueTitle.append(issueData[i]['title'])
            issueBody.append(issueData[i]['body'])
            issueState.append(issueData[i]['state'])
            i+=1

        issueLink = "https://api.github.com/repos/" + githubRepo + "/issues?state=all&page=" +  str(issuePageIncrement)
        print("issueLink: " + issueLink)
        issuePageIncrement+=1


        with urllib.request.urlopen(Request(issueLink, data=None, headers=testHeader, origin_req_host=None, unverifiable=False, method=None)) as url:
            issueData = json.loads(url.read().decode())
        accumulatedIssues+=len(issueData)
        print("acumulatedIssues:" + str(accumulatedIssues))

    if DEBUG:
        print("\tnumber of issues found by pagination: " + str(len(issueID)))
        print("\tissue author: " + str(issueAuthor))
        print("\tissueID: " + str(issueID))
        print("\tcreated at: " + str(dateIssueCreated))
        print("\tIssue title: " + str(issueTitle))

    #write issue information to CSV file
    if WRITE:
        print("Writing Issues to CSV file.....")
        i = 0
        with open('githubIssueInformation.csv', mode='w') as issueFile:
            issueWriter = csv.writer(issueFile, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
            issueWriter.writerow(['Repository','Issue ID', 'Issue Title' 'Issue Author', 'Issue Body', 'Created At'])
            for i in range(numIssues):
                issueWriter.writerow([name, issueID[i], issueTitle[i].encode("utf-8"), issueAuthor[i], issueBody[i].encode("utf-8"), dateIssueCreated[i]])

    #make space for memory
    del issueID[:]
    del issueTitle[:]
    del issueAuthor[:]
    del issueBody[:]
    del dateIssueCreated[:]
else:
    #releases
    releaseLink = githublink + "/releases?pages=1"
    if DEBUG:
        print(releaseLink)

    i = 0
    releaseData = []
    releaseAuthors = []
    releaseName = []
    releaseNodeID = []
    releaseNumber = []
    hasReleases = True
    releasePublishDate = []
    releasePageIncrement = 2

    with urllib.request.urlopen(Request(releaseLink, data=None, headers=testHeader, origin_req_host=None, unverifiable=False, method=None)) as url:
        releaseData = json.loads(url.read().decode())

    if len(releaseData) == 0:
        hasReleases = False
    else:
        numRelease = len(releaseData)

    if hasReleases:
        while len(releaseData) != 30: 
            i = 0
            while i < len(releaseData):
                releaseAuthors.append(releaseData[i]['author']['login'])
                releaseName.append(releaseData[i]['name'])
                releaseNodeID.append(releaseData[i]['node_id'])
                releaseNumber.append(releaseData[i]['id'])
                releasePublishDate.append(releaseData[i]['published_at'])
                i+=1

            releaseLink = githublink + "/releases?page=" + str(releasePageIncrement)
            releasePageIncrement+=1

            with urllib.request.urlopen(releaseLink) as url:
                releaseData = json.loads(url.read().decode())
            numRelease+=len(releaseData)

    #release information
    if WRITE and hasReleases:
        i = 0
        with open('githubReleaseInformation.csv', mode='w') as releaseFile:
            releaseWriter = csv.writer(releaseFile, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
            releaseWriter.writerow(['Github Name','Node ID', 'ID', 'Author', 'Name', 'Date Published'])
            for i in range(numRelease):
                releaseWriter.writerow([name, releaseNodeID[i], releaseNumber[i], releaseAuthors[i], releaseName[i], releasePublishDate[i]])

    #clear up release memory
    del releaseAuthors[:]
    del releaseName[:]
    del releaseNodeID[:]
    del releaseNumber[:]
    del releasePublishDate[:]

#general information
if WRITE:
    with open('githubInformation.csv', mode='w') as githubFile:
        githubWriter = csv.writer(githubFile, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        githubWriter.writerow(['Github Name', 'Node ID', 'URL', 'Date of Creation', 'Date Updated', 'Number of Stars', 'Number of Watchers', 'Number of Forks', 'Number of Issues', 'Number of Releases', 'License'])
        githubWriter.writerow([name, id, githubURL, creationDate, updateDate, str(numStars), str(numWatchers), str(numForks), numIssues, str(numRelease), licenseName])

print("Done")