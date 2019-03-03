import os, subprocess, pygit2, sys, git, csv
from git import Repo
from pygit2 import clone_repository

if __name__ == "__main__":
    repo_path = os.getenv('GIT_REPO_PATH')
    repo = Repo(repo_path)
    if not repo.bare:
        print('Repo at {} successfully loaded.'.format(repo_path))
        commits = list(repo.iter_commits('master'))
        with open('githubCommitInformation.csv', mode='w+') as commitFile:
                commitWriter = csv.writer(commitFile, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
                commitWriter.writerow(['Commit SHA', 'Author', 'Commit Message', 'Date of Commit', 'Count', 'Size'])
                for commit in commits:
                    commitWriter.writerow([str(commit.hexsha), str(commit.author.name).encode("utf-8"), str(commit.summary).encode("utf-8"), str(commit.authored_datetime), str(commit.count()), str(commit.size)])
                    pass
    else:
        print('Could not load repository at {} :('.format(repo_path))

        # todo: add count and size to csv file