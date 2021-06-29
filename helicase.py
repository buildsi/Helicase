from pydriller import Repository
from git import Repo
from datetime import *

class Helicase:
    def analyze(self, commit):
        return

    def traverse(self, path:str, since:datetime=None, to:datetime=None, checkout:bool=False, printTrial:bool=False):
        repo = Repo(path)

        if printTrial:
            count = 0
            for commit in Repository(path, since=since, to=to).traverse_commits():
                count += 1
            i = 0
        for commit in Repository(path, since=since, to=to).traverse_commits():
            if checkout:
                repo.git.checkout(commit.hash)
            if printTrial:
                i += 1
                print(f"Analyzing Commit [{i}/{count}]", flush=True)
            self.analyze(commit)
    