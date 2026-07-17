#Fastapis built in tool for ttesting
#lets your tests send fake requests to your app without actually starting uvicorn or opening a real port
from fastapi.testclient import TestClient
from app.main import app

#wraps your app object so you can call client.get() client.post()
#just like a real HTTP client
client = TestClient(app)

#pytest automatically finds and runs any function starting with test_
#assert response.satsus_code == 201
#assert means this must be true or fail the test
def test_create_task():
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 999
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] == False
    assert data["id"] is not None


def test_get_tasks():
    client.post("/tasks", json={"title": "Walk the dog"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_single_task():
    #first create a post to create a task 
    #get the id of the task you created
    create_response = client.post("/tasks", json={"title": "Read a book"})
    task_id = create_response.json()["id"]

    #now fecth the task you just created
    response = client.get(f"/tasks/{task_id}")
    #has to be 200 else fail the test
    assert response.status_code == 200
    #the response has to be the task just created else failed
    assert response.json()["title"] == "Read a book"


def test_get_nonexistent_task():
    response = client.get("/tasks/9999")
    #try fetching a task that does not exist
    assert response.status_code == 404


def test_complete_task():
    create_response = client.post("/tasks", json={"title": "Do laundry"})
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] == True