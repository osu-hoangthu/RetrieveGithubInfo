import urllib.request, json
import sys
import csv

DEBUG = 1 #allows to see output of all information
WRITE = 0 #locks/unlocks the ability to write it into .csv files

if  len(sys.argv) <= 1:
    print("No repository given")
    exit()

githubRepo =  str(sys.argv[1])

githublink = "https://api.github.com/repos/" + githubRepo

if DEBUG:
    print("concatenated githublink: " + githublink)

with urllib.request.urlopen(githublink) as url:
    data = json.loads(url.read().decode())

name = data['name']
id = data['node_id']
creationDate = data['created_at']
updateDate = data['updated_at']
numStars = data['stargazers_count']
numWatchers = data['watchers_count']
numForks = data['forks_count']
numIssues = data['open_issues']
license = data['license']
hasLicense = True
if license is None:
    hasLicense = False
    licenseName = "None"
else:
    licenseName = data['license']['name']
githubURL = data['url']
pushedDate = data['pushed_at']
numIssues = data['open_issues_count']

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

commitsLink = githublink + "/commits"
if DEBUG:
    print("github commit link: " + commitsLink)

with urllib.request.urlopen(commitsLink) as url:
    commitData = json.loads(url.read().decode())

numCommits = len(commitData)
commitSHA = []
authors = []
commitMsg = []
commitDates = []
i = 0

for i in range(numCommits):
    commitSHA.append(commitData[i]['sha'])
    authors.append(commitData[i]['commit']['author']['name'])
    commitMsg.append(commitData[i]['commit']['message'])
    commitDates.append(commitData[i]['commit']['author']['date'])
    i += 1

if DEBUG:
    print("\tnumber of commits: " + str(numCommits))
    print("\tSha:" + str(commitSHA))
    print("\tAuthor: " + str(authors))
    print("\tcommit messages: " + str(commitMsg))
    print("\tdate: " + str(commitDates))

issueLink = githublink + "/issues?per_page=100"
if DEBUG:
    print(issueLink)

with urllib.request.urlopen(issueLink) as url:
    issueData = json.loads(url.read().decode())


i = 0
issueBody = []
issueTitle = []
dateIssueCreated = []
issueID = []
issueAuthor = []

for i in range(numIssues):
    if DEBUG:
            print(i)
    issueAuthor.append(issueData[i]['user']['login'])
    issueID.append(issueData[i]['node_id'])
    dateIssueCreated.append(issueData[i]['created_at'])
    issueTitle.append(issueData[i]['title'])
    issueBody.append(issueData[i]['body'])

if DEBUG:
    print("\tnumber of issues: " + str(numIssues))
    print("\tissue author: " + str(issueAuthor))
    print("\tissueID: " + str(issueID))
    print("\tcreated at: " + str(dateIssueCreated))
    print("\tIssue title: " + str(issueTitle))

releaseLink = githublink + "/releases"
if DEBUG:
    print(releaseLink)

releaseData = []
releaseAuthors = []
releaseName = []
releaseNodeID = []
releaseNumber = []
hasReleases = True

with urllib.request.urlopen(releaseLink) as url:
    releaseData = json.loads(url.read().decode())

if len(releaseData) == 0:
    hasReleases = False


#general information
if WRITE:
    with open('githubInformation.csv', mode='w') as githubFile:
        githubWriter = csv.writer(githubFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        githubWriter.writerow(['Github Name', 'Node ID', 'URL', 'Date of Creation', 'Date Updated', 'Number of Stars', 'Number of Watchers', 'Number of Forks', 'Number of Issues', 'Number of Commits', 'Number of Issues', 'License'])
        githubWriter.writerow([name, id, githubURL, creationDate, updateDate, str(numStars), str(numWatchers), str(numForks), numIssues, numCommits, numIssues, licenseName])

#commit information
if WRITE:
    i = 0
    with open('githubCommitInformation.csv', mode='w') as commitFile:
        commitWriter = csv.writer(commitFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        commitWriter.writerow(['Commit SHA', 'Author', 'Commit Message', 'Date of Commit'])
        for i in range(numCommits):
            commitWriter.writerow([commitSHA[i], authors[i], commitMsg[i], commitDates[i]])
            i+=1

#issue information
if WRITE:
    i = 0
    with open('githubIssueInformation.csv', mode='w') as issueFile:
        issueWriter = csv.writer(issueFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        issueWriter.writerow(['Issue ID', 'Issue Title' 'Issue Author', 'Issue Body', 'Created At'])
        for i in range(numIssues):
            issueWriter.writerow([issueID[i], issueTitle[i], issueAuthor[i], issueBody[i].encode("utf-8"), dateIssueCreated[i]])