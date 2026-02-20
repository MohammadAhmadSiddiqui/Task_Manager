from fastapi import FastAPI, HTTPException
from app.database import task_collection
from app.models import Task
from bson import ObjectId

app = FastAPI()

def task_serializer(task):
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"],
        "created_at": task["created_at"]
    }

@app.post("/tasks")
def create_task(task: Task):
    result = task_collection.insert_one(task.dict())
    return {"id": str(result.inserted_id)}

@app.get("/tasks")
def get_tasks():
    tasks = task_collection.find()
    return [task_serializer(task) for task in tasks]

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = task_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_serializer(task)

@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    result = task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    result = task_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
