class DummyUser(object):
 
    def get_and_delete_messages(self):
        pass
 
class NeedsUserObject(object):
 
    def process_request(self, request):
        request.user = DummyUser()
