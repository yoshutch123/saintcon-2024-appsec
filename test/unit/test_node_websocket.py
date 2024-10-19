import requests
import utils
from websockets.sync.client import connect
from websocket import WebSocketTimeoutException
import json
import datetime
import time

def wait_for_message(ws, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            message = ws.recv()
            return message
        except WebSocketTimeoutException:
            time.sleep(0.1)
    raise TimeoutError("Message not received in time")

class TestWebsocket:
    JAVA_API = "http://irc.local:1337/api"
    WEBSOCKET = "ws://irc.local:1337/ws"

    def test_connect_to_websocket(self):
        # user 1
        response = utils.createUser()
        cookies1 = response.cookies
        user1 = response.json()
        response = requests.post(f"{self.JAVA_API}/rooms", json={"name":"roomba"}, cookies=cookies1)
        roomId = response.json().get("roomId")

        # user 2
        response = utils.createUser()
        cookies2 = response.cookies
        user2 = response.json()
        response = requests.post(f"{self.JAVA_API}/rooms/{roomId}/users", cookies=cookies1, json={"username":user2.get("username"), "roomId":roomId})
        token1 = requests.get(f"{self.JAVA_API}/connect/{roomId}", cookies=cookies1).text

        token2 = requests.get(f"{self.JAVA_API}/connect/{roomId}", cookies=cookies2).text

        ws1 =  connect(f"{self.WEBSOCKET}/?user={user1.get("userId")}&token={token1}",
            additional_headers={"Cookie": "auth=" + cookies1.get("auth"), "Origin":"http://irc.local"})
        ws2 = connect(f"{self.WEBSOCKET}/?user={user2.get("userId")}&token={token2}",
            additional_headers={"Cookie": "auth=" + cookies2.get("auth"), "Origin":"http://irc.local"})
        ws1.send(json.dumps({"text": "huzzah", "timestamp":datetime.datetime.now().timestamp()}))
        message1 = wait_for_message(ws1)
        message2 = wait_for_message(ws2)
        assert message1 is not None
        msg1 = json.loads(message1)[0]
        msg2 = json.loads(message2)[0]
        assert msg1.get("text") == msg2.get("text") == "huzzah"
        assert msg1.get("userId") == msg2.get("userId") == str(user1.get("userId"))
        ws1.send(json.dumps({"text": "last", "timestamp":datetime.datetime.now().timestamp()}))
        for i in range(9):
            ws1.send(json.dumps({"text": str(i), "timestamp":datetime.datetime.now().timestamp()}))
                

        time.sleep(2)
        ws1 = connect(f"{self.WEBSOCKET}/?user={user1.get("userId")}&token={token1}&count=10",
            additional_headers={"Cookie": "auth=" + cookies1.get("auth"), "Origin":"http://irc.local"})
        prev_messages = json.loads(ws1.recv())
        assert len(prev_messages) > 0
        found = False
        for msg in prev_messages:
            if msg["text"] == "last":
                found = True
                break

        assert found


   