import pytest
from fastapi.testclient import TestClient
from todo_fastapi.app.main import app

# Fixture to provide a test client for the FastAPI application.
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Fixture to automatically clean up the test database before each test runs.
@pytest.fixture(autouse=True)
def clean_up(client):
    # Clean up the database by deleting all todo items.
    client.delete("/todos/")

# Test to verify that creating a todo item works correctly.

def test_create_todo(client):
    response = client.post("/todos/", json={"title": "NewTask"})
    assert response.status_code == 200
    assert response.json() == {"title": "NewTask", "description": None, "completed": False}

# Test to check if fetching from an empty database returns an empty list.

def test_fetch_all_empty_database(client):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []

# Test to verify fetching all todos returns the correct data.
def test_fetch_all(client):
# Simulate posting a new todo item
    client.post("/todos/", json={"title": "NewTask"})
    
    # Fetch all todos and check for correct serialization
    response = client.get("/todos/")
    assert response.status_code == 200
    todos = response.json()
    assert todos[0]['title'] == "NewTask"
    assert isinstance(todos[0]['id'], str)  # Check if 'id' is correctly serialized as string



# Test to verify fetching a non-existent todo returns a 404 error.

def test_fetch_one_not_in_database(client):
    response = client.get("/todos/Learn FastAPI")
    assert response.status_code == 404
    assert response.json() == {"detail": "{title} was not found"}

# Test to verify fetching a specific existing todo item works as expected.

def test_fetch_one(client):
    client.post("/todos/", json={"title": "NewTask"})
    response = client.get("/todos/NewTask")
    assert response.status_code == 200
    assert response.json() == {"title": "NewTask", "description": None, "completed": False}

# Test to verify updating a non-existent todo returns a 404 error.

def test_update_todo_not_in_database(client):
    response = client.put("/todos/NewTask", json={"title": "NewTask1"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo with title 'NewTask' not found or not updated"}

# Test to verify that updating an existing todo item works correctly.

def test_update_todo(client):
    client.post("/todos/", json={"title": "NewTask"})
    response = client.put("/todos/NewTask", json={"title": "NewTask1", "description": "Updated task", "completed": True})
    assert response.status_code == 200
    assert response.json() == {"title": "NewTask1", "description": 'Updated task', "completed": True}

# Test to verify that attempting to delete a non-existent todo returns a 404 error.

def test_remove_todo_not_in_database(client):
    response = client.delete("/todos/NewTask")
    assert response.status_code == 404
    assert response.json() == {'detail': '{title} was not found'}

# Test to verify that deleting an existing todo works correctly.

def test_remove_todo(client):
    client.post("/todos/", json={"title": "NewTask"})
    response = client.delete("/todos/NewTask")
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully deleted NewTask"}

# Test to verify that deleting all todos in the database works correctly.

def test_remove_all(client):
    client.post("/todos/", json={"title": "NewTask"})
    client.post("/todos/", json={"title": "NewTask1"})
    response = client.delete("/todos/")
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully deleted all todos"}
