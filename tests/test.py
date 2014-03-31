from app import app
from nose.tools import with_setup
import json

class Test_App:
    def setup(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        print "Setting up!"

    def test_status_code(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_search(self):
        searchstring1 = '/search/\xe9\xb1\xbc\xe9\xa6\x99\xe8\x8c\x84\xe5\xad\x90'
        searchstring2 = '/search/\xe5\xae\xab\xe7\x88\x86\xe9\xb8\xa1\xe4\xb8\x81'
        searchstring3 = '/search/\xe7\x89\x9b\xe8\x82\x89\xe6\x8b\x89\xe9\x9d\xa2'

        response = self.app.get(searchstring1)
        assert response.status_code == 200
        data = json.loads(response.data)
        data = json.loads(response.data)
        try:
            translation = data['translation']
            assert translation
        except KeyError:
            print "Wrong data returned - no translation."

        response = self.app.get(searchstring2)
        assert response.status_code == 200
        data = json.loads(response.data)
        try:
            chin = data['dish'][0]
            eng = data['dish'][1]
            assert chin['data'] == u'\u5bab\u7206\u9e21\u4e01'
            assert eng['data'] == 'gong bao chicken'

        except KeyError:
            print "Wrong data returned - no dish."

        response = self.app.get(searchstring3)
        assert response.status_code == 200
        data = json.loads(response.data)
        try:
            translation = data['translation']
            assert translation
            similar = data['similar']
            assert similar
        except KeyError:
            print "Wrong data returned - no translation or no similar."

    def test_upload(self):
        image1 = './tests/images/image1.png'
        image2 = './tests/images/image2.png'
        print "Entered test_upload"
        with open(image2) as f:
            img_data = f.read()

        print "Sending request."
        response = self.app.post('/upload', data=img_data)
        assert response.status_code == 302

        with open(image1) as f:
            img_data = f.read()

        response = self.app.post('/upload', data=img_data)
        assert response.status_code == 302
