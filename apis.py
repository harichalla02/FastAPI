from fastapi import FastAPI
from models import Users

app = FastAPI()

users = [
        Users(id=1, name="Tony", email="tony@gmail.com", city="Hyderabad"),
        Users(id=2, name="Hari", email="hari@gmail.com", city="Bangalore"),
        Users(id=3, name="Ravi", email="ravi@gmail.com", city="Guntur"),
        Users(id=4, name="Ramesh", email="ramesh@gmail.com", city="Chennai"),
        Users(id=5, name="Suresh", email="suresh@gmail.com", city="Mumbai")
    ]

@app.get('/users')
def get_all():
    return users

@app.get('/user/{id}')
def get_By_ID(id:int):
    for i in range(len(users)):
        if users[i].id == id:
            return users[i]
    return "User not found"

@app.post('/user')
def create_User(user:Users):
    users.append(user)
    return user

@app.put('/user')
def update_user(id:int, user:Users):
    for i in range(len(users)):
        if users[i].id == id:
            users[i] = user
            return "User updated sucessfully"
    return "User not found"

@app.delete('/user')
def delete_user(id:int):
    for i in range(len(users)):
        if users[i].id == id:
            del users[i]
            return "User deleted"
    return "User not found"