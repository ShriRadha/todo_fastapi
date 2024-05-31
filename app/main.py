from fastapi import FastAPI, HTTPException
from . import crud, schemas


app = FastAPI()

@app.post("/todos/", response_model=schemas.TodoSchema)
async def create_todo(todo: schemas.TodoSchema):
    return await crud.create_todo(todo)


@app.get("/todos/")
async def fetch_all():
    return await crud.fetch_all()

@app.get("/todos/{title}", response_model=schemas.TodoSchema)
async def fetch_one(title: str):
    todo = await crud.fetch_one(title)
    if todo is not None:
        return todo
    else:
        raise HTTPException(status_code=404, detail="{title} was not found")

@app.put("/todos/{title}", response_model=schemas.TodoSchema)
async def update_todo(title: str, todo: schemas.UpdateTodo):
    updated_todo = await crud.update_todo(title, todo)
    if updated_todo:
        return updated_todo
    else:
        raise HTTPException(status_code=404, detail="{title} was not found")

    

@app.delete("/todos/{title}")
async def remove_one(title: str):
    deleted = await crud.remove_one(title)
    if deleted:
        return {"message": f"Successfully deleted {title}"}
    else:
        raise HTTPException(status_code=404, detail="{title} was not found")


@app.delete("/todos/")
async def remove_all():
    deleted = await crud.remove_all()
    if deleted:
        return {"message": "Successfully deleted all todos"}
    else:
        raise HTTPException(status_code=404, detail="No todos to delete")