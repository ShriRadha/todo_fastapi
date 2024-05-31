from fastapi import HTTPException
from .databaseinfo import db
from bson import ObjectId
from todo_fastapi.app.schemas import TodoSchema, UpdateTodo


#Create
def create_todo(todo: TodoSchema):
    document = todo.model_dump()
    result = db.insert_data(document)
    return document

def doc_to_dict(document):
    """Convert a MongoDB document or a Pydantic model into a dictionary that can be serialized to JSON."""
    if isinstance(document, dict):
        # Convert all ObjectId instances to strings to ensure JSON serializability
        document_dict = {k: str(v) if isinstance(v, ObjectId) else v for k, v in document.items()}
        # Rename '_id' to 'id'
        if '_id' in document_dict:
            document_dict['id'] = document_dict.pop('_id')
        return document_dict
    elif isinstance(document, TodoSchema):
        # Assuming TodoSchema is a Pydantic model
        return document.model_dump(by_alias=True)  # Ensure aliases are used if set in Pydantic model
    else:
        raise TypeError("Document conversion expects a dictionary or a TodoSchema instance.")




#Read All
def fetch_all():
    cursor = db.fetch_data({})
    return [doc_to_dict(todo) for todo in cursor]

#Read One
def fetch_one(title: str):
    todo = db.fetch_data({"title": title})
    if todo is not None and len(todo) > 0:
        return doc_to_dict(todo[0])
    else:
        return None

#Update
def update_todo(title: str, todo: UpdateTodo):
    update_data = todo.model_dump(exclude_unset=True)
    update_result = db.update_data({"title": title}, update_data)
    if update_result == 0:
        raise HTTPException(status_code=404, detail=f"Todo with title '{title}' not found or not updated")
    
    updated_todos = db.fetch_data({"title": update_data.get("title", title)})
    if not updated_todos:
        raise HTTPException(status_code=404, detail="The updated todo could not be retrieved.")
    
    updated_todo = updated_todos[0]  # Correct handling of list
    return doc_to_dict(updated_todo)



#Delete
def remove_one(title: str):
    delete_result = db.delete_data({"title": title})
    return delete_result > 0  # Ensure deleted_count is being accessed correctly

#Delete all
def remove_all():
    delete_result = db.delete_all_data({})
    return delete_result > 0
