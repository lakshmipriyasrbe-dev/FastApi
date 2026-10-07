from fastapi import FastAPI, Depends, HTTPException
from schemas import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Todo

Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency Function for db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#post Route - Create Todo
@app.post("/todos", response_model=TodoSchema)
def create(todo:TodoCreate, db: Session=Depends(get_db)):
    db_todo = Todo(**todo.dict()) # convert pydantic data into dictionary type in python
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo) # once data stored, it will get that data
    return db_todo # Json 

#get Alll datas

@app.get("/todos", response_model=list[TodoSchema])
def read_todos(db: Session=Depends(get_db)):
    return db.query(Todo).all()

#get Single data

@app.get('/todos/{todo_id}',response_model=TodoSchema)
def read_todo(todo_id:int, db: Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Todo Not Found')
    return todo

# put request - updated todo
@app.put('/todos/{todo_id}', response_model=TodoSchema)
def update_todo(todo_id:int, updated: TodoCreate, db: Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
            raise HTTPException(status_code=404, detail='Todo Not Found')
    for key,value in updated.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

# delete data
@app.delete("/todos/{id}")
def delete_todo(id:int, db: Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Todo Not Found')
    db.delete(todo)
    db.commit()
    return {"message": "Todo Deleted Successfully"}