from fastapi import FastAPI
from fastapi import HTTPException
import mysql.connector as con

app = FastAPI()

db = con.connect(
    host="localhost",
    user="root",
    password="Pranith$7981",
    database="studentdb"
)

cur = db.cursor()

cur.execute("create table if not exists studenttbl(id int primary key auto_increment, name varchar(50), age int, grade varchar(2))")

@app.get("/student")
def total_students():
    cur.execute("SELECT * FROM studenttbl")
    data = cur.fetchall()
    return data

@app.get("/student/{id}")
def get_student(id: int):
    cur.execute(f"SELECT * FROM studenttbl WHERE id = {id}")
    data = cur.fetchall()
    return data

@app.post("/student")
def add_student(name: str, age: int, grade: str):
    post = "insert into studenttbl(name, age, grade) values(%s, %s, %s)"
    data=(name, age, grade)
    cur.execute(post, data)
    db.commit()
    return {"status": "Added successfully"}

@app.put("/student/{id}")
def update_student(id: int, name: str, age: int, grade: str):
    put = "update studenttbl set name = %s, age = %s, grade = %s where id = %s"
    data = (name, age, grade, id)
    cur.execute(put, data)
    db.commit()
    return {"status": "Updated successfully"}


@app.delete("/student/{id}")
def delete_student(id: int):
    delete = "delete from studenttbl where id = %s"
    data = (id,)
    cur.execute(delete, data)
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    db.commit()
    return {"status": "Deleted successfully"}