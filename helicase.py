from datetime import *
import subprocess
import re
import sys
import os
import contextlib
import dateutil.parser
from dataclasses import dataclass

@contextlib.contextmanager
def working_dir(directory):
    pwd = os.getcwd()
    os.chdir(directory)
    yield pwd
    os.chdir(pwd)

@dataclass
class Repo:
    git_repo_dir:str

    def __init__(self, git_repo_dir=os.getcwd()):
        self.git_repo_dir = git_repo_dir

    def git(self, *args, split=True):
        cmd = ["git"]
        cmd.extend(args)

        with working_dir(self.git_repo_dir):
            output = subprocess.check_output(cmd)
            output = output.decode("utf-8")
            if split:
                output = output.strip().split("\n")
            return output

    def linear_history(self, from_commit, to_commit, length=sys.maxsize):
        """Yield tuples of (commit, date) on the current branch, from newest to
        oldest.  Date used is commit date, because it is monotonic."""
        result = []
        output = self.git("log", "--first-parent", "--no-merges", "--format=%H %aI %cI", f"{from_commit}...{to_commit}")
        for i, line in enumerate(output):
            if i >= length:
                break
            commit, author_date, committer_date = re.split(r"\s+", line)
            result.append(Commit(commit, dateutil.parser.parse(author_date), dateutil.parser.parse(committer_date), self))
        
        result.reverse()
        return result

@dataclass
class Commit:
    hash: str
    author_date: datetime
    committer_date: datetime
    repo: Repo

    def modified_files(self, length=sys.maxsize):
        result = []
        output = self.repo.git("diff", "--name-status", f"{self.hash}~1...{self.hash}")
        for i, line in enumerate(output):
            if i >= length:
                break
            change_type, path = re.split(r"\s+", line)
            result.append(File(change_type, path))
        return result

@dataclass
class File:
    change_type: str
    path: str

    def __init__(self, change_type, path):
        self.change_type = change_type
        self.path = path

    def __str__(self) -> str:
        return f"{self.change_type}\t{self.path}"
        

class Helicase:
    def analyze(self, commit):
        return

    def traverse(self, path:str, since:datetime=None, from_commit:str=None, to:datetime=None, to_commit:str=None, checkout:bool=False, printTrial:bool=False):
        repo = Repo(path)
        commits = repo.linear_history(from_commit=from_commit, to_commit=to_commit)
        count = len(commits)
        i = 0

        for commit in commits:
            # If the commit exists in more branches than just the main branch that very
            # likely means that it was committed in a separate branch and merged in later
            # which is not what we want to analyze.
            if checkout:
                repo.git("checkout", commit.hash)
            if printTrial:
                i += 1
                print(f"Analyzing Commit [{i}/{count}]", flush=True)
            self.analyze(commit)