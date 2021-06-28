from pydriller import Repository
from git import Repo
from datetime import *

class Helicase:
    def analyze(self, commit):
        return

    def traverse(self, path:str, since:datetime=None, to:datetime=None, checkout:bool=False):
        repo = Repo(path)

        for commit in Repository(path, since=since, to=to).traverse_commits():
            if checkout:
                repo.git.checkout(commit.hash)
            self.analyze(commit)
    