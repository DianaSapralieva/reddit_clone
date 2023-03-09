from v4_user import schemas

def test_create_post(authorized_client):
    res = authorized_client.post(
        "/posts/", json={"title": "My title", "content": "My content", "author": "test user"})
		# verify the schema and allow autocompletion
    created_post = schemas.BlogPost_Response(**res.json())
    assert res.status_code == 201
    assert created_post.title == "My title"
    assert created_post.content == "My content"
    assert created_post.author == "test user"
    assert created_post.published == True

#Test get one post
# def test_get_one_post(authorized_client, created_post):
#     res = authorized_client.get(f"/posts/{created_post.id}")
#     print(res.json())
#     post = schemas.BlogPost_Response(**res.json())
#     assert post.BlogPost.id == created_post.id
#     assert post.BlogPost.content == created_post.content
#     assert post.BlogPost.title == created_post.title

#Test get all the posts
def test_get_posts(authorized_client):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
