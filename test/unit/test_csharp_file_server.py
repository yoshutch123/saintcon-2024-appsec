import requests
import uuid
import os

class TestCSharpFileServer:
    URL = f"http://{os.environ['irc']}:1337/files"

    def test_file_upload_download_image(self):
        file_content = """<svg height="100" width="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" /></svg>"""
        files = {'file': file_content}
        filename = str(uuid.uuid4()) + ".svg"
        response = requests.post(self.URL + "/upload", files=files, data={"filename":filename})
        assert 200 <= response.status_code <= 300
        filename = response.text

        response = requests.get(self.URL + "/?path=" + filename)
        assert response.status_code == 200
        assert response.text == file_content
        assert "attachment" not in response.headers.get("Content-disposition", "").lower()
        assert response.headers.get("Content-type") == "image/svg+xml"

    def test_file_upload_download_txt(self):
        file_content = "my note"
        files = {'file': file_content}
        filename = str(uuid.uuid4()) + ".txt"
        response = requests.post(self.URL + "/upload", files=files, data={"filename":filename})
        assert 200 <= response.status_code <= 300
        assert filename in response.text

        response = requests.get(self.URL + "/?path=" + filename)
        assert response.status_code == 200
        assert response.text == file_content
        assert "attachment" in response.headers.get("Content-disposition", "").lower()
        assert response.headers.get("Content-type") == "text/plain"