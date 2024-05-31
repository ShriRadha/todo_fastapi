from .database import todo_collection
from .schemas import TodoSchema, UpdateTodo
from fastapi import HTTPException

#Create
async def create_todo(todo: TodoSchema):
    document = todo.model_dump()
    result = await todo_collection.insert_one(document)
    return document

def doc_to_dict(document):
    """Convert a MongoDB document or a custom object into a dictionary that can be serialized to JSON."""
    # Check if the document is already a dictionary
    if isinstance(document, dict):
        doc_dict = document.copy()  # Make a copy to avoid modifying the original
    else:
        # Attempt to convert using the .dict() method, assuming it's a custom object (like a Pydantic model)
        doc_dict = document.dict()
    # For example, converting '_id' from ObjectId to string, if necessary
    if '_id' in doc_dict:
        doc_dict['_id'] = str(doc_dict['_id'])
    return doc_dict

#Read All
async def fetch_all():
    cursor = todo_collection.find({})
    return [doc_to_dict(todo) async for todo in cursor]

#Read One
async def fetch_one(title: str):
    todo = await todo_collection.find_one({"title": title})
    if todo is not None:
        return doc_to_dict(todo)
    else:
        return None

#Update
async def update_todo(title: str, todo: UpdateTodo):
    update_data = todo.model_dump(exclude_unset=True)
    update_result = await todo_collection.update_one({"title": title}, {"$set": update_data})
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"Todo with title {title} not found or not updated")
    updated_todo = await todo_collection.find_one({"title": update_data.get("title", title)})
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="The updated todo could not be retrieved.")
    return doc_to_dict(updated_todo)

#Delete
async def remove_one(title: str):
    delete_result = await todo_collection.delete_one({"title": title})
    return delete_result.deleted_count > 0

#Delete all
async def remove_all():
    delete_result = await todo_collection.delete_many({})
    return delete_result.deleted_count > 0
