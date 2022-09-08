import requests


class TestServer:
    def test_store(self):
        r=requests.post("http://127.0.0.1:5000/testcase_store",json={"id":"888","case_step":"hahaah"})
        assert r.status_code==200
    def test_get(self):
        r=requests.get("http://127.0.0.1:5000/testcase_get",params={'id':777})
        assert r.status_code==200