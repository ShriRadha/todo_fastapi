import pytest
from unittest.mock import MagicMock, patch
from todo_fastapi.app.crud import create_todo, fetch_all, fetch_one, update_todo, remove_one, remove_all
from todo_fastapi.app.schemas import TodoSchema, UpdateTodo


# Test case for the create_todo function to ensure it correctly inserts a new todo item.
@patch("todo_fastapi.app.crud.db.insert_data")
def test_create_todo(mock_todo_collection):
    # Prepare a TodoSchema object as the input for the create_todo function.
    todo = TodoSchema(title="NewTask")
    # Mock the insert_one method of the todo_collection to return the prepared TodoSchema object.
    mock_todo_collection.insert_one = MagicMock()
    mock_todo_collection.insert_one.return_value = todo
    # Execute the create_todo function and assert that the result matches the expected model dump.
    result = create_todo(todo)
    assert result == todo.model_dump()

# Class to mock the async iterator behavior of MongoDB's find method.
class AsyncIteratorWrapper:
    def __init__(self, items):
        self._items = items

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return self._items.pop(0)
        except IndexError:
            raise StopAsyncIteration



# Test case for fetch_all function to ensure it can retrieve all todo items.
@patch("todo_fastapi.app.crud.db.fetch_data")
def test_fetch_all(mock_fetch_data):
    # Prepare a dictionary to simulate a database record.
    todo_dict = {"title": "NewTask", "description": None, "completed": False}
    # Set up MagicMock to iterate over a list of dictionaries.
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter([todo_dict])
    mock_fetch_data.return_value = mock_cursor
    # Execute fetch_all and assert that the returned list matches the expected model dumps.
    result = fetch_all()

    assert result == [todo_dict]


# Test case for fetch_one function to ensure it can retrieve a single todo item by title.
@patch("todo_fastapi.app.crud.db.fetch_data")
def test_fetch_one(mock_find_one):
    # Prepare a TodoSchema object to simulate a found database record.
    todo = TodoSchema(title="NewTask")
    # Mock the find_one method to return the prepared TodoSchema object.
    mock_find_one.return_value = [todo.model_dump()]  # Assuming fetch_one expects a dictionary
    # Execute fetch_one with a specific title and assert the result matches the expected model dump.
    result = fetch_one("NewTask")
    assert result == todo.model_dump()

# Test case for update_todo function to ensure it can update a todo item correctly.
@patch("todo_fastapi.app.crud.db")
def test_update_todo(mock_db):
    # Setup
    updated_todo_dict = {"title": "NewTask1"}
    mock_db.update_data.return_value = MagicMock(modified_count=1)
    mock_db.fetch_data.return_value = [updated_todo_dict]  # Return a list with one item
    
    # Execute the update_todo function
    result = update_todo("NewTask", UpdateTodo(title="NewTask1"))
    
    # Verify that the result matches the expected model dump
    assert result == updated_todo_dict

 

@patch("todo_fastapi.app.crud.db.delete_data")
def test_remove_one(mock_delete_data):
    # Configure the MagicMock to return an integer representing the count of deleted documents
    mock_delete_data.return_value = 1  # Return 1 to indicate one document was successfully deleted
    
    # Execute remove_one with a specific title and assert that it returns True for successful deletion.
    result = remove_one("NewTask")
    assert result == True

# Test case for remove_all function to ensure it can remove all todo items.
@patch("todo_fastapi.app.crud.db.delete_all_data")
def test_remove_all(mock_delete_all_data):
    # Mock the delete_all_data method to simulate a successful deletion operation for all items.
    mock_delete_all_data.return_value = 1
    
    # Execute remove_all and assert that it returns True for successful deletion.
    result = remove_all()
    assert result == True
