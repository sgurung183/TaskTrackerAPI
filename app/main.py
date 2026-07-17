from fastapi import FastAPI, HTTPException
from app.models import Task

app = FastAPI()

tasks: list[Task] = [] #list of tasks empty list
next_id = 1 #id of the next task

# "@"" is the decorator in python
# these attach extra behavior to the function right below then
# here it tells FastApi to wire this funciton up to handle GET requests 
# at "/tasks" same as @GetMapping("/tasks")
#FastApi automatically converst the list into a JSON array
@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks", status_code = 201)
def create_task(task: Task): #the parameter typed as Task is how FastAPI knows to parse the incoming JSON body into a Task object
    #only type hint needed unlike springboot whre u needed annotation
    global next_id #when you want to modify a variable outside the functionyou need the global keyword
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}") #path parameter, FastAPI captures whatever is in that URL segment
def get_task(task_id: int): #fucntion parameter should match the {task_id}
    for task in tasks:
        if task.id == task_id:
            return task
    #loop through the list to find matching id if nothing found the exception
    raise HTTPException(status_code = 404, detail = "Task not found")

@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            return task
    raise HTTPException(status_code = 404, detail = "Task was not found")
        
    