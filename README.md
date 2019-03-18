# RetrieveGithubInfo
This project gets a repository through command line argument and calls Github API parses the JSON and places that information into different .csv files. If the function calls are successful, then there will be four different .csv files: general Github information, Commits, Releases, and Issues. The general Github information .csv file is a file that gathers all of the information that is displayed on the main page on the repository which are: Github Name, Node ID, URL, Date of Creation, Date Updated, Number of Stars, Number of Watchers, Number of Forks, Number of Issues, Number of Commits, Number of Issues, License (if applicable). The Commits .csv file will gather all information of the Github commits which are: Commit SHA, Author, Commit Message, and Date of Commit. The Issue .csv file will gather all of the information on the Issues which are: Issue ID, Issue Title, Issue Author, Issue Body, and Created At (the date the issue was created).

## Motivation
This repository is originally made to help Assistant Professor Shaokun Fan with this research in cryptocurrency. The information taken from a Github repository are the basic information, the commits, and the issues (both open and closed issues) and parses the recieved JSON and puts them into separate .csv files.

## How to use
1) Clone the repository using the HTTP link:
`git clone https://github.com/osu-hoangthu/RetrieveGithubInfo.git`
2) Run the command:
`python getGithubAPIJson.py <Github-User>/<Repository-Name> <Github Token> <issue/release>`
Note: without designating the Github username, number of tokens, and the Repository name, the program will not get any information. Instead it will print out `Not enough information given.` and will exit the program without making any calls or creating .csv files. The choice between creating the issue or release .csv file must be chosen in order to avoid GitHub API's rate limit.