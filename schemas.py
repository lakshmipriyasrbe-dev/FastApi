from pydantic import BaseModel

class TodoBase(BaseModel):
    title : str
    description : str | None = None
    completed : bool = False

class TodoCreate(TodoBase): # inside of () was base of this class
    pass

class Todo(TodoBase):
    id: int
    class Config:        # for Convert python Object to JSON data
        orm_mode = True