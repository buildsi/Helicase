# Helicase
Helicase is a Library for Unravelling and Parsing Git Histories

## Usage
To use Helicase create a class in Python which inherits from the Helicase class. From there you can define your custom `analyze()` function and then call the `traverse()` method when you are ready to iterate through the commit history.

##### Without Checking Out The Repository
```python
from helicase import Helicase
from datetime import *

class PrintCommits(Helicase):
    def analyze(self, commit):
        print(commit.hash)


dt = datetime(2021, 6, 18)
now = datetime.now()

pc = PrintCommits()
pc.traverse("../../Spack/spack", since=dt, to=now)
```

##### Checking Out The Repository

```python
from helicase import Helicase
from datetime import *

class PrintCommits(Helicase):
    def analyze(self, commit):
        print(commit.hash)
        result = subprocess.run(["../../Spack/spack/bin/spack", "--version"], capture_output=True, text=True)
        print(result)


dt = datetime(2021, 6, 18)
now = datetime.now()

pc = PrintCommits()
pc.traverse("../../Spack/spack", since=dt, to=now, checkout=True)
```