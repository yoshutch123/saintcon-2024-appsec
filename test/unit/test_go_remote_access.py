import socket

class TestGoRemoteAccess:

    def test_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("remote-access", 8023))
        assert b"Username:" in s.recv(1024)
        s.send(b"sketrik\n")
        assert b"Password:" in s.recv(1024)
        s.send(b"sekure\n")
        result = s.recv(1024)
        assert b"successful auth" in result and b"sketrik" in result
        s.send(b"whoami\n")
        assert b"root" in s.recv(1024)
        s.send(b"exit!\n")
        s.close()