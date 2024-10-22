import requests
import utils
import os

class TestJavaApi:
    URI = f"http://{os.environ['irc']}:1337/api"

    def test_user_create_and_login(self):
        response = utils.createUser()
        assert response.status_code == 201
        assert response.cookies.get_dict().get("auth") is not None
        assert response.json().get("name") == "John Doe"
        uname = response.json().get("username")
        assert uname is not None
        response = requests.post(self.URI + "/login", json={"username":uname, "password":"password1"})
        assert response.cookies.get_dict().get("auth") is not None
        assert response.json().get("name") == "John Doe"
        assert response.json().get("username") == uname

    def test_get_user_self(self):
        response = utils.createUser()
        d = response.json()
        uid = d.get("userId")
        username = d.get("username")
        name = d.get("name")
        assert uid is not None
        print(response.cookies.get_dict())
        response = requests.get(self.URI + "/users/" + str(uid), cookies=response.cookies.get_dict())
        assert response.status_code == 200
        assert response.json().get("username") == username
        assert response.json().get("name") == name
        
    def test_create_get_room(self):
        room_name = "myroom"
        response = utils.createUser()
        cookies = response.cookies.get_dict()
        response = requests.post(self.URI + "/rooms", json={"name":room_name}, cookies=cookies)
        assert response.status_code == 201
        d = response.json()
        assert d['name'] == room_name
        
        response = requests.get(f"{self.URI}/rooms/{d.get("roomId", "")}", cookies=cookies)
        assert response.status_code == 200
        assert d['name'] == room_name

    def test_get_rooms(self):
        room_name1 = "myroom1"
        room_name2 = "myroom2"
        response = utils.createUser()
        cookies = response.cookies.get_dict()
        id1 = requests.post(self.URI + "/rooms", json={"name":room_name1}, cookies=cookies).json().get("roomId")
        id2 = requests.post(self.URI + "/rooms", json={"name":room_name2}, cookies=cookies).json().get("roomId")
        
        response = requests.get(f"{self.URI}/rooms", cookies=cookies)
        assert response.status_code == 200
        d = response.json()
        assert set([x['roomId'] for x in d]).issuperset(set([id1, id2]))
        assert set([x['name'] for x in d]).issuperset(set([room_name1, room_name2]))
        
    def test_add_get_delete_users_in_room(self):
        room_name = "room_with_users"
        response = utils.createUser()
        cookies = response.cookies.get_dict()
        response = requests.post(self.URI + "/rooms", json={"name":room_name}, cookies=cookies)
        roomId = response.json().get("roomId")
        user2 = utils.createUser().json()
        response = requests.post(f"{self.URI}/rooms/{roomId}/users", json={"username":user2.get("username"), "roomId":roomId}, cookies=cookies)
        assert response.status_code == 201
        d = response.json()
        assert d.get("userId") == user2.get("userId")
        assert d.get("username") == user2.get("username")


        user3 = utils.createUser().json()
        response = requests.post(f"{self.URI}/rooms/{roomId}/users", json={"username":user3.get("username"), "roomId":roomId}, cookies=cookies)
        assert response.status_code == 201
        d = response.json()
        assert d.get("userId") == user3.get("userId")
        assert d.get("username") == user3.get("username")

        response = requests.get(f"{self.URI}/rooms/{roomId}/users", cookies=cookies)
        assert response.status_code == 200
        users = response.json()
        assert set([x['userId'] for x in users]).issuperset(set([user2.get("userId"), user3.get("userId")]))


        # get user in my room
        response = requests.get(f"{self.URI}/users/{user3.get('userId')}", cookies=cookies)
        assert response.status_code == 200
        assert response.json().get("username") == response.json().get("username")

        # remove user from my room
        response = requests.delete(f"{self.URI}/rooms/{roomId}/users/{user3.get('userId')}", cookies=cookies)
        assert response.status_code == 204
        response = requests.get(f"{self.URI}/rooms/{roomId}/users", cookies=cookies)
        assert user3.get("userId") not in {x['userId'] for x in response.json()}
