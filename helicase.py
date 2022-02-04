from pydriller import Repository
from git import Repo
from datetime import *

class Helicase:
    def analyze(self, commit):
        return

    def traverse(self, path:str, since:datetime=None, from_commit:str=None, to:datetime=None, to_commit:str=None, checkout:bool=False, printTrial:bool=False):
        repo = Repo(path)

        if printTrial:
            count = 0
            for commit in Repository(path, since=since, from_commit=from_commit, to=to, to_commit=to_commit, only_in_branch=repo.active_branch.name, only_no_merge=True).traverse_commits():
                count += 1
            i = 0
        for commit in Repository(path, since=since, from_commit=from_commit, to=to, to_commit=to_commit, only_in_branch=repo.active_branch.name, only_no_merge=True).traverse_commits():
            # If the commit exists in more branches than just the main branch that very
            # likely means that it was committed in a separate branch and merged in later
            # which is not what we want to analyze.
            if repo.active_branch.name not in commit.branches or len(commit.branches) > 1:
                continue
            if checkout:
                repo.git.checkout(commit.hash)
            if printTrial:
                i += 1
                print(f"Analyzing Commit [{i}/{count}]", flush=True)
            self.analyze(commit)
    