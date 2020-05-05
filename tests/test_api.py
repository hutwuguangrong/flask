import json
import unittest


from sqlalchemy.util import b64encode

from app import db, create_app, Role, User


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        response = self.client.get('/api/v1/posts/', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_post(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='www@qq.com', password='123456', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/api/v1/posts/', headers=self.get_api_headers('www@qq.com', '123456'),
                                    data=json.dumps({'body': 'body of the *blog* post'}))
        self.assertEqual(response.status_code, 201)

        url = response.headers.get('Location')
        self.assertIsNotNone(url)
        response = self.client.get(url, headers=self.get_api_headers('www@qq.com', '123456'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual('http://localhost'+json_response['url'], url)



