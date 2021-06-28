from helicase import Helicase
from datetime import *

class PrintCommits(Helicase):
    def analyze(self, commit):
        print(commit.hash)


dt = datetime(2021, 6, 18)
now = datetime.now()

pc = PrintCommits()
pc.traverse("../../Spack/spack", since=dt, to=now)