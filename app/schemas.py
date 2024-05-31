from pydantic import BaseModel, Field
from typing import Optional

class TodoSchema(BaseModel):
    title: str = Field(...)
    description: Optional[str] = None
    completed: bool = Field(default=False)

    class Config:
        schema_extra = {
            "example": {
                "title": "Learn FastAPI",
                'description': "Learn how to use FastAPI and create a small project",
                "completed": True
            }
        }
    
class UpdateTodo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Learn FastAPI",
                'description': "Learn how to use FastAPI and create a small project",
                "completed": True
            }
        }
