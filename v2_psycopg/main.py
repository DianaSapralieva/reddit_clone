from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor


# Database connection
try:
    connection = psycopg2.connect(
        host='localhost',
        database='reddit_clone',
        user='postgres',
        password='API',
        cursor_factory= RealDictCursor
    )
    cursor = connection.cursor()
    print('Database connection successful')
except Exception as error:
    print('Database connection failed')
    print('Error', error)
    
# Pydantic schema for POST Body (sent by Client) validation
class BlogPost(BaseModel):
    title: str
    content: str
    author: str
    rating: Optional[int] = None
    published: bool = True

# API instance name
app = FastAPI()


##################################
#########    ENDPOINTS    ########
##################################

# GET ALL BLOGPOSTS
@app.get("/posts")
def get_posts():
    # Writing the SQL query
    cursor.execute("SELECT * FROM posts")
    # Retrieving all the posts (list)
    database_posts = cursor.fetchall()
    # Return database posts in JSON
    return {"data" : database_posts }

# CREATE NEW BLOGPOST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: BlogPost):
    cursor.execute("INSERT INTO posts (title, content, author, published, rating ) "+
                   "VALUES(%s,%s,%s,%s,%s) RETURNING *", 
                   (new_post.title,new_post.content,new_post.author,new_post.published,new_post.rating) )
    new_post = cursor.fetchone()
    connection.commit() # Save the changes to the Database
    return {"data": new_post}

# GET POST BY ID
@app.get("/posts/{id_param}")
def get_post(id_param: int, response: Response):
    # Get post by ID logic
    #write SQL query
    id_string = str(id_param)
    print(id_string)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id_string,))
    corresponding_row = cursor.fetchone()
    #HTTP exception
    if not corresponding_row:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"No corresponding post was for id: {id_param} "
        )
    return {"Retrieved row": corresponding_row} #corresponding blogpost

@app.delete("/posts/{id_param}")
def delete_post(id_param: int):
    # deleting post 
    id_param_str = str(id_param)
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id_param_str,))
    row = cursor.fetchone()
    connection.commit()
    if not row :
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"No corresponding post was for id: {id_param} "
        )
    return Response (status_code = status.HTTP_204_NO_CONTENT)

# replaces post with given ID and request body
@app.put("/posts/{id_param}")
def replace_post(id_param: int, updated_post: BlogPost):
    # updating post logic
    cursor.execute("Update posts SET title = %s, content = %s, author = %s, rating = %s, published = %s WHERE id = %s RETURNING *",
                   (updated_post.title, updated_post.content, updated_post.author, updated_post.rating, updated_post.published, id_param))
    update_post = cursor.fetchone()
    connection.commit()
    if not update_post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"No corresponding post was for id: {id_param} "
        )
    return update_post #updated blogpost

