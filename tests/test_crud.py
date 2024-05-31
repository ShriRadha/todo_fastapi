import pytest
from unittest.mock import AsyncMock, patch
from app.crud import create_todo, fetch_all, fetch_one, update_todo, remove_one, remove_all
from app.schemas import TodoSchema, UpdateTodo


# Test case for the create_todo function to ensure it correctly inserts a new todo item.
@pytest.mark.asyncio
@patch("app.crud.todo_collection")
async def test_create_todo(mock_todo_collection):
    # Prepare a TodoSchema object as the input for the create_todo function.
    todo = TodoSchema(title="NewTask")
    # Mock the insert_one method of the todo_collection to return the prepared TodoSchema object.
    mock_todo_collection.insert_one = AsyncMock()
    mock_todo_collection.insert_one.return_value = todo
    # Execute the create_todo function and assert that the result matches the expected model dump.
    result = await create_todo(todo)
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
@pytest.mark.asyncio
@patch("app.crud.todo_collection")
async def test_fetch_all(mock_todo_collection):
    # Prepare a TodoSchema object to simulate a database record.
    todo = TodoSchema(title="NewTask")
    # Mock the find method to return an async iterator over the prepared todo items.
    mock_todo_collection.find.return_value = AsyncIteratorWrapper([todo])
    # Execute fetch_all and assert that the returned list matches the expected model dumps.
    result = await fetch_all()
    assert result == [todo.model_dump()]

# Test case for fetch_one function to ensure it can retrieve a single todo item by title.
@pytest.mark.asyncio
@patch("app.crud.todo_collection")
async def test_fetch_one(mock_todo_collection):
    # Prepare a TodoSchema object to simulate a found database record.
    todo = TodoSchema(title="NewTask")
    # Mock the find_one method to return the prepared TodoSchema object.
    mock_todo_collection.find_one = AsyncMock()
    mock_todo_collection.find_one.return_value = todo
    # Execute fetch_one with a specific title and assert the result matches the expected model dump.
    result = await fetch_one("NewTask")
    assert result == todo.model_dump()

# Test case for update_todo function to ensure it can update a todo item correctly.
@pytest.mark.asyncio
@patch("app.crud.todo_collection")
async def test_update_todo(mock_todo_collection):
    # Prepare a TodoSchema object as the original todo item.
    todo = TodoSchema(title="NewTask")
    # Mock the update_one method to simulate a successful update operation.
    mock_todo_collection.update_one = AsyncMock()
    mock_todo_collection.update_one.return_value.modified_count = 1
    # Mock the find_one method to return the updated TodoSchema object.
    mock_todo_collection.find_one = AsyncMock()
    mock_todo_collection.find_one.return_value = todo
    # Execute update_todo with a new title and assert the result matches the expected model dump.
    result = await update_todo("NewTask", UpdateTodo(title="NewTask1"))
    assert result == todo.model_dump()

# Test case for remove_one function to ensure it can remove a single todo item.
@pytest.mark.asyncio
@patch("app.crud.todo_collection")
async def test_remove_one(mock_todo_collection):
    # Mock the delete_one method to simulate a successful deletion operation.
    mock_todo_collection.delete_one = AsyncMock()
    mock_todo_collection.delete_one.return_value.deleted_count = 1
    # Execute remove_one with a specific title and assert that it returns True for successful deletion.
    result = await remove_one("NewTask")
    assert result == True

# Test case for remove_all function to ensure it can remove all todo items.
@pytest.mark.asyncio
@patch("app.crud.todo_collection")
async def test_remove_all(mock_todo_collection):
    # Mock the delete_many method to simulate a successful deletion operation for all items.
    mock_todo_collection.delete_many = AsyncMock()
    mock_todo_collection.delete_many.return_value.deleted_count = 1
    # Execute remove_all and assert that it returns True for successful deletion.
    result = await remove_all()
    assert result == True
