
# my first python unit test with unittest

import unittest

from app.jutebag.backend import JutebagBackend

class TestJutebagBackend(unittest.TestCase):

    cred_file_path = "cred/jutebag-py-firebase-cred.json"
    store = JutebagBackend(cred_file_path)


    def test_returns_bag_for_hm10(self):
        bag = self.store.fetchBag("moritz.maus@hm10.net")
        self.assertEquals([0, 1, 2], bag["some"])
        self.assertTrue(len(bag["bagData"]) > 10)

    def test_returns_bag_for_gmail(self):
        bag = self.store.fetchBag("h.moritz.maus@gmail.com")
        self.assertEquals([0, 1, 2], bag["some"])
        self.assertTrue(len(bag["bagData"]) > 3)

    def test_returns_empty_bag_for_unknown_user(self):
        # currently fails because the todo-id lookup fails (when trying to access the user data)
        bag = self.store.fetchTodo('foofoo@barbar')
        self.assertEquals(0, len(bag['tasks']))
        self.assertEquals(1, bag['version'])

    
    def test_returns_todo_list_for_hm10(self):
        """
        FIXME: create proper tests
        """
        bag = self.store.fetchTodo('moritz.maus@hm10.net')
        self.assertEquals(0, len(bag['tasks']))
        self.assertEquals(2, bag['version'])

    def test_generates_todolist_id_for_hm10(self):
        todoId_1 = self.store._todoId('moritz.maus@hm10.net')
        todoId_2 = self.store._todoId('moritz.maus@hm10.net')
        self.assertEquals(todoId_1, todoId_2)

    def test_store_todo_list(self):
        #     """
        #     Demo to setup test data.
        #     FIXME: create proper tests!
        #     """
        #     todo_data = {
        #         'version' : 2,
        #         'tasks': []
        #     }
        # todo_data_2 = {"version":1,
        #     "tasks":[
        #         {"taskList":[
        #             {"status":0,"label":"Aufgabe 1"},
        #             {"status":0,"label":"Aufgabe 2"}],
        #             "nextActionTime":"2021-01-26T07:00:18.394Z","label":"Task 1"},
        #             {"taskList":[
        #                 {"status":0,"label":"Konto aufmachen"}],
        #                 "nextActionTime":"2021-01-25T19:52:11.938Z",
        #                 "label":"Geld"}]
        #                 }
        # self.store.storeTodo('moritz.maus@hm10.net', todo_data_2)
        pass





