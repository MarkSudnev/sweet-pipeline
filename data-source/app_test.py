from app import app


class TestApp:

    test_app = ...

    def setup_method(self):
        self.test_app = app.test_client()
        self.test_app.testing = True

    def test_returns_ok_when_query_is_present_and_correct(self):
        response = self.test_app.get("/data?q=hello")
        assert response.status == '200 OK'
        assert response.data.decode() == '{"query": "hello", "response": "some response data"}'

    def test_returns_bad_request_when_query_is_missing(self):
        response = self.test_app.get("/data?abcd=hello")
        assert response.status.lower() == '400 bad request'

