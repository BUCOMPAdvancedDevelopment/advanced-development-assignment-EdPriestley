from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    def test_about (self):
        tester=app.test_client(self)
        response=tester.get('/about', content_type='html/text')
        self.assertEqual(response.status_code,200)

    def test_account(self):
        tester = app.test_client(self)
        response = tester.get('/account', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_afterAmend(self):
        tester = app.test_client(self)
        response = tester.get('/afterAmend', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_afterDelete(self):
        tester = app.test_client(self)
        response = tester.get('/afterDelete', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_afterOrder(self):
        tester = app.test_client(self)
        response = tester.get('/afterOrder', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_amendOrder(self):
        tester = app.test_client(self)
        response = tester.get('/amendOrder', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_deleteOrder(self):
        tester = app.test_client(self)
        response = tester.get('/deleteOrder', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_newOrder(self):
        tester = app.test_client(self)
        response = tester.get('/newOrder', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_signUp(self):
        tester = app.test_client(self)
        response = tester.get('/signUp', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_userOrder(self):
        tester = app.test_client(self)
        response = tester.get('/userOrder', content_type='html/text')
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
