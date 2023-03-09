from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# find next unique ID
def next_id_jacky(posts:List):
    last_item = posts[len(posts)-1] #last item in my list
    id_last = last_item["id"]
    return id_last+1

# find and return the post with a given ID
def find_post(given_id):
    for post in my_blog_posts:
        if post["id"] == given_id:
            return post

# find and return the index with a given ID
def find_post_index(given_id):
    for index,post in enumerate(my_blog_posts):
        if post["id"] == given_id:
            return index





# Pydantic schema for POST Body (sent by Client) validation
class BlogPost(BaseModel):
    title: str
    content: str
    author: str
    rating: Optional[int] = None
    published: bool = True

# API instance name
app = FastAPI()

# List of Blog Posts (Local list)
my_blog_posts = [{"id": 1,"Title" : "Welcome to our class","content" : "reddit post","Author":"Bob the constructor"},
                 {"id": 2,"Title" : "2nd session","content" : "cat food","Author":"Felix the cat"}]


##################################
#########    ENDPOINTS    ########
##################################

# GET ALL BLOGPOSTS
@app.get("/posts")
def get_posts():
    return {"data" : my_blog_posts }

# CREATE NEW BLOGPOST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: BlogPost, response: Response):
    post_dict = new_post.dict() #convert new_post to dictionary
    tmp_dict = {"id": next_id_jacky(my_blog_posts)} #define temp dictionary with new key
    tmp_dict.update(post_dict) #merging two dictionaries together
    my_blog_posts.append(tmp_dict)
    return {"message":f"New blog post added with title: {new_post.title}"}

# GET POST BY ID
@app.get("/posts/{id_param}")
def get_post(id_param: int, response: Response):
    corresponding_post = find_post(id_param)
    if not corresponding_post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"No corresponding post was for id: {id_param} "
        )
    return {"data": corresponding_post}


@app.delete("/posts/{id_param}")
def delete_post(id_param: int):
    # deleting post logic
    # 1. find the index
    corresponding_index = find_post_index(id_param)
    if not corresponding_index:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"No corresponding post was for id: {id_param} "
        )
    # 2. Remove element from List
    my_blog_posts.pop(corresponding_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# replaces post with given ID and request body
@app.put("/posts/{id_param}")
def replace_post(id_param: int, updated_post: BlogPost):
    #updating logic
    # 1. find the index
    corresponding_index = find_post_index(id_param)
    if not corresponding_index:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"No corresponding post was for id: {id_param} "
        )
    # Transform the data from the body (pydantic class) to a dictionary
    updated_post_dict = updated_post.dict() 
    # add ID
    updated_post_dict["id"] = id_param
    # replace blog post with updated_post_dict
    my_blog_posts[corresponding_index] = updated_post_dict
    return updated_post_dict

