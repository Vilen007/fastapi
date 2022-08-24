from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title : str
    description : str
    status : bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='12345678', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection Established")
        break
    except Exception as e:
        print("Connecting Failed")
        print("Error: ", e)
        time.sleep(2)
all_post = []
def find(id):
    for i in all_post:
        if i['id'] == id:
            return i


@app.get('/sqlalchemy')
async def root(db: Session = Depends(get_db)):
    return {'message': "message"}

@app.get('/posts')
async def get_post():
    cursor.execute(''' SELECT * from posts ''')
    posts = cursor.fetchall()
    return {'Data' :  posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def news(post: Post):
    cursor.execute(""" INSERT INTO posts (title,description,status) VALUES (%s, %s, %s) RETURNING * """, (post.title,post.description,post.status))
    postNew = cursor.fetchone()
    conn.commit()
    return {'Data' :  postNew}

@app.get('/posts/latest')
async def get_post():
    cursor.execute(""" SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    postNew = cursor.fetchone()
    return {'Data' :  postNew}

@app.get('/posts/{id}')
async def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
    postNew = cursor.fetchone() 
    if not postNew:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Not Found")
    return {'Data' :  postNew}

@app.delete('/posts/{id}' , status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    postDel = cursor.fetchone()
    conn.commit()
    if not postDel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Not Found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
async def update_post(id: int , post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, description = %s , status = %s WHERE id = %s RETURNING * """,(post.title,post.description,post.status,str(id)))
    postup = cursor.fetchone()
    conn.commit()
    if not postup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Not Found")
    return {'Data' :  postup}