from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_hw():
	r = client.get('/isEven/2')

	assert r.status_code == 200
	assert r.json() == {'isEven': True}