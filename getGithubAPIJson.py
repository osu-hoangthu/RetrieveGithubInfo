import urllib.request, json
import sys

DEBUG = 1

if  len(sys.argv) <= 1:
    print("No link given")
    exit()

githublink =  str(sys.argv[1])

githublink = "https://api.github.com/repos/" + githublink

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
if license != '/0':
    hasLicense = True
    licenseName = data['license']['name']
pushedDate = data['pushed_at']

if DEBUG:
    print("name: " + name)
    print("node ID: " + id)
    print("creation date: " + creationDate)
    print("update date: "  + updateDate)
    print("num stars: " + str(numStars))
    print("num watchers: " + str(numWatchers))
    print("num forks: " + str(numForks))
    print("number of issues: " + str(numIssues))
    print("url: " + githubURL)
    if hasLicense:
        print(licenseName)
    print("latest commit: " + pushedDate)

print("done")