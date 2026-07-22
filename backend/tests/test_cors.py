from fastapi.testclient import TestClient

from app.main import app


class CorsTests:
    def test_allows_frontend_origin_for_preflight(self):
        client = TestClient(app)
        response = client.options(
            "/dial-in-sessions/",
            headers={
                "Origin": "http://127.0.0.1:3000",
                "Access-Control-Request-Method": "POST",
            },
        )

        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:3000"
