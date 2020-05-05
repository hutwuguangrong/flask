import unittest

from flask import current_app

from app import create_app, db, Role, User


class FLASKClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)  # 如果启用了use_cookies就可以像浏览器一样发送cookies

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_400_page(self):
        response = self.client.get('/nothing')  # 访问一个未定义的url
        data = response.get_data(as_text=True)
        self.assertIn('Not Found wgr', data)
        self.assertEqual(response.status_code, 404)

    def test_register_and_login(self):
        response = self.client.post('/auth/register', data={
            'email': '419259833@qq.com',
            'username': 'f',
            'password': '123456',
            'password2': '123456'
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/auth/login', data={
            'email': '419259833@qq.com',
            'password': '123456'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(email='419259833@qq.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token), follow_redirects=True)
        user.confirm(token)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have confirmed your account' in response.get_data(as_text=True))

        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)






