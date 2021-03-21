from firebase_admin import credentials
import firebase_admin 
import firebase_admin.firestore as firestore
import uuid
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1.collection import CollectionReference


# used to avoid multiple initializations, which wouldn't work with firebase
initialized = {}

class JutebagBackend(object):

    cred = None
    firestore_db = None

    def __init__(self, credentials_file_path):
        if not credentials_file_path in initialized:
            print("initializing firebase")
            cred = credentials.Certificate(credentials_file_path)
            initialized[credentials_file_path] = firebase_admin.initialize_app(cred)
            print("firebase initialized")
        self.firestore_db = firestore.client()


    def _createBagId(self, userEmail: str) -> str:
        """Create and register a bagId for the user with the given email
        Args:
            userEmail: the user id (email)
        
        Returns:
            a uuid string representing the (random) generated and registered bagID
        """
        bagId: str = uuid.uuid4().hex
        self.firestore_db.document(u'users', userEmail).set({'bagId' : bagId}, merge=True)
        return bagId

    def _createTodoId(self, userEmail: str) -> str:
        """Create and register a todoId for the user with the given email
        Args:
            userEmail: the user id (email)
        
        Returns:
            a uuid string representing the (randomly) generated and registered todoID
        """
        bagId: str = uuid.uuid4().hex
        self.firestore_db.document(u'users', userEmail).set({'todoId' : bagId}, merge=True)
        return bagId

    def _bagId(self, userEmail: str) -> str:
        userData = self.firestore_db.document(u'users', userEmail).get().to_dict()
        return userData['bagId'] if 'bagId' in userData else self._createBagId(userEmail)

    def _todoId(self, userEmail: str) -> str:
        # FIXME: what to do if user does not exist?
        userData = self.firestore_db.document(u'users', userEmail).get().to_dict()
        return userData['todoId'] if 'todoId' in userData else self._createTodoId(userEmail)

    def _getBag(self, userEmail: str) -> DocumentReference:
        return self.firestore_db.document(u'bags', self._bagId(userEmail), u'shoppingBag', u'latest')

    def _getBag_v2(self, userEmail: str) -> DocumentReference:
        return self.firestore_db.document(u'bags', self._bagId(userEmail), u'shoppingBag2', u'latest')

    def _getTodo(self, userEmail: str) -> DocumentReference:
        return self.firestore_db.document(u'todos', self._todoId(userEmail), u'todoList', u'latest')

    def _getPendingJoinRequests(self, userEmail: str) -> CollectionReference:
        return self.firestore_db.collection(u'bags', self._bagId(userEmail), u'joinRequests')

    def storeBag_v1(self, userEmail: str, storeData: dict) -> dict:
        """
        Stores the bag to firestore. Overwrites any existing stuff
        """
        self._getBag(userEmail).set(storeData)
        return {"revision" : 1}

    def fetchBag_v1(self, userEmail: str) -> dict:
        """
        Retrieves the bag and returns it as string
        """
        return self._getBag(userEmail).get().to_dict()

    def storeBag_v2(self, userEmail: str, storeData: dict) -> dict:
        """
        Stores the bag to firestore. Overwrites any existing stuff
        """
        self._getBag_v2(userEmail).set(storeData)
        return {"revision" : 1}

    def fetchBag_v2(self, userEmail: str) -> dict:
        """
        Retrieves the bag and returns it as string
        """
        return self._getBag_v2(userEmail).get().to_dict()



    def getJoinRequests(self, userEmail: str) -> list:
        result = []
        count = 0
        for req in self._getPendingJoinRequests(userEmail).list_documents():
            result.append(req.get().to_dict())
            count = count + 1
            if count > 10: # hard limit to counter DoS
                break

        return result

    def addJoinRequest(self, userEmail: str, requestedJoinEmail: str) -> str:
        joinRequestData = {
            'requester' : userEmail,
        }
        requestCollection = self._getPendingJoinRequests(requestedJoinEmail)

        # remove potential duplicates
        # TODO: checkout query API ad
        count = 0
        for existingReq in requestCollection.list_documents():
            req = existingReq.get().to_dict()
            if req.get('requester') == userEmail:
                print("Deleting one exsting join request")
                existingReq.delete()
            count = count + 1
            if count > 10:
                break
        requestCollection.add(joinRequestData)

        return "ok"


    ###
    ###  FIXME
    ###  That stuff (TodoList treatment) should not be part of the Jutebag backend, that's the whole point!
    ###  Excuse: it went in there since I personally urgently needed that feature, and I'm willing to properly
    ###  redesign it later.
    ###

    def fetchTodo(self, userEmail: str) -> dict:
        """ Fetch and return the todo list for the given user or return an empty (matching) object.
        """
        todo_doc = self._getTodo(userEmail).get()
        print("todo = " + str(todo_doc))
        print("todo_dict = " + str(todo_doc.to_dict()))
        todo_dict = todo_doc.to_dict()
        if todo_dict == None:
            return {
                'version' : 1,
                'tasks' : []
            }
        return {
            'version' : todo_dict['version'] if 'version' in todo_dict else 1,
            'tasks' : todo_dict['tasks'] if 'tasks' in todo_dict else []
            }

    def storeTodo(self, userEmail: str, todoData: dict) -> dict:
        """
        returns always {'revision' : 1}
        """
        self._getTodo(userEmail).set(todoData)
        return {"revision" : 1}

