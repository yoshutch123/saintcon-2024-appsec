import requests
import utils
import psycopg2
import os

class TestRubyAdmin:
    URI = f"http://{os.environ['irc']}:1337/admin"

    def test_admin_login(self):
        response = utils.createUser()
        username = response.json()['username']
        conn = psycopg2.connect(database="postgres",
                                host="postgresql",
                                user="postgres",
                                password="password",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET role='admin' WHERE username='{username}';")
        conn.commit()

        response = requests.post(f"{self.URI}/login", data={"username":username, "password":"password1"}, allow_redirects=False)
        assert 400 > response.status_code >= 200
        response = requests.get(f"{self.URI}/dashboard", cookies=response.cookies.get_dict())
        assert "User Dashboard" in response.text

    def test_ban_user(self):
        response = utils.createUser()
        admin = response.json()['username']
        conn = psycopg2.connect(database="postgres",
                                host="postgresql",
                                user="postgres",
                                password="password",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET role='admin' WHERE username='{admin}';")
        conn.commit()

        response = requests.post(f"{self.URI}/login", data={"username":admin, "password":"password1"}, allow_redirects=False)
        admin_cookies = response.cookies.get_dict()

        response = utils.createUser()
        username = response.json()["username"]
        user_to_ban = response.json()['userId']
        response = requests.post(f"{self.URI}/ban", json={"userId":user_to_ban}, cookies = admin_cookies)
        assert 300 > response.status_code >= 200
        response = requests.post(f"http://{os.environ['irc']}:1337/api/login", json={"username":username, "password":"password1"})
        assert response.status_code >= 400


    def test_unban_user(self):
        response = utils.createUser()
        admin = response.json()['username']
        conn = psycopg2.connect(database="postgres",
                                host="postgresql",
                                user="postgres",
                                password="password",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET role='admin' WHERE username='{admin}';")
        conn.commit()

        response = requests.post(f"{self.URI}/login", data={"username":admin, "password":"password1"}, allow_redirects=False)
        admin_cookies = response.cookies.get_dict()

        response = utils.createUser()
        username = response.json()["username"]
        user_to_ban = response.json()['userId']
        response = requests.post(f"{self.URI}/ban", json={"userId":user_to_ban}, cookies = admin_cookies)
        response = requests.post(f"{self.URI}/unban", json={"userId":user_to_ban}, cookies = admin_cookies)
        response = requests.post(f"http://{os.environ['irc']}:1337/api/login", json={"username":username, "password":"password1"})
        assert 400 > response.status_code >= 200

        
