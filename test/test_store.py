
# my first python unit test with unittest

import unittest

from app.jutebag.store import Store

class TestJutebagStore(unittest.TestCase):

    def test_returns_something(self):
        store = Store()
        testResult = store.testIt()
        self.assertEquals("yeah", testResult)

