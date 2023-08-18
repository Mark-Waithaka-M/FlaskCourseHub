import unittest
from flask import Flask
from flask_testing import TestCase
from app import create_app as _create_app

class myTest(TestCase):
    def create_app(self):
        app = _create_app()
        app.config['TESTING'] = True
        return app
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assert200(response)
        

    def test_login_page(self):
        response = self.client.post('/login',data = dict(email = 'djonte0@gmail.com',password = '1234567890'))
        self.assert200(response)


    