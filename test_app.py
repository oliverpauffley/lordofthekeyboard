from app import app


def test_index():
    app.testing = True

    tester = app.test_client()
    response = tester.get("/")

    assert response.status_code == 200
