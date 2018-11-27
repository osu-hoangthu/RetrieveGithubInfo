import urllib.request, json
import sys

DEBUG = 1

if  len(sys.argv) <= 1:
    print("No repository given")
    exit()

githubRepo =  str(sys.argv[1])

githublink = "https://api.github.com/repos/" + githubRepo

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
hasLicense = False
githubURL = data['url']
if str(license) is None:
    hasLicense = True
    licenseName = data['license']['name']
pushedDate = data['pushed_at']

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
        print("\t" + licenseName)
    print("\tlatest commit: " + pushedDate)

commitsLink = githublink + "/commits"
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

issueLink = githublink + "/issues"
print(issueLink)

with urllib.request.urlopen(issueLink) as url:
    issueData = json.loads(url.read().decode())

numIssues = len(issueData)
i = 0
issueBody = []
issueTitle = []
dateIssueCreated = []
issueID = []
issueAuthor = []

for i in range(numIssues):
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
    #print("\tissue body: " + str(issueBody))
    print("\tIssue title: " + str(issueTitle))

print("done")