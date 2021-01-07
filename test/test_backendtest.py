
# my first python unit test with unittest

import unittest

from app.jutebag.backend import JutebagBackend

class TestJutebagBackend(unittest.TestCase):

    cred_file_path = "src/cred/jutebag-py-firebase-cred.json"
    store = JutebagBackend(cred_file_path)


    def test_returns_bag_for_hm10(self):
        bag = self.store.fetchBag("moritz.maus@hm10.net")
        self.assertEquals([0, 1, 2], bag["some"])
        self.assertTrue(len(bag["bagData"]) > 10)

    def test_returns_bag_for_gmail(self):
        bag = self.store.fetchBag("h.moritz.maus@gmail.com")
        self.assertEquals([0, 1, 2], bag["some"])
        self.assertTrue(len(bag["bagData"]) > 3)
    
    def test_returns_todo_list_for_hm10(self):
        """
        FIXME: create proper tests
        """
        bag = self.store.fetchTodo('moritz.maus@hm10.net')
        self.assertEquals(0, len(bag['tasks']))
        self.assertEquals(1, bag['revision'])




