
# Test if Fast API is running
def test_docs(client):
    res = client.get("/docs")
    print(res.status_code)
    assert res.status_code == 200

def test_redoc(client):
    res = client.get("/redoc")
    print(res.status_code)
    assert res.status_code == 200
