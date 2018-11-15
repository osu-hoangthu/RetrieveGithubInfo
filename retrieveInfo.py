#!/usr/bin/python

import sys
import git #allows github link to be pulled
from git import Repo

DEBUG = 1

if  len(sys.argv) <= 1:
    print("No link given")
    exit()

githublink =  str(sys.argv[1])

Repo.clone_from(githublink, "test") #clone repo and place it into a directory called "test"
repo = git.Repo(search_parent_directories=True)

# gets number of branches
numBranches = len(repo.branches)

if DEBUG:
    print("number of branches: " + str(numBranches))
    print("commmit message: " + str(numCommits))