## singleton-py

type-parameterized singleton decorator (PEP 695 compliant). zero dependencies. works 
with all modern type-checkers. tested in python 3.14.6, although i do not see why it 
wouldn't work just fine over the entire python 3.x surface.

### how to set it up

1. `git clone https://github.com/nk-rt/singleton-py.git`
2. create a class and put the decorator thing on it

```python
from singleton import singleton

# all attributes & methods are transparently proxied
@singleton
class Database:
    def __init__(self, host="localhost", port=5432):
        self.host = host
        self.port = port

# first call always wins
db1 = Database()
# all consecutive attempts to instantiate return the same instance
db2 = Database()

# see i told you
assert db1 is db2
```

3. yeah, that's about all there is to it

`:)`
