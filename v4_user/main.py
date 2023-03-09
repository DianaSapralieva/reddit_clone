from fastapi import FastAPI
from . import models #. means current folder
from .database import database_engine  #. means current folder
from .routers import posts_router, users_router, auth_router

#Create the tables if they don't exist yet
models.Base.metadata.create_all(bind=database_engine)  

# API instance name
app = FastAPI()

#include the posts router
app.include_router(posts_router.router)

#include the users router
app.include_router(users_router.router)

#include the auth router
app.include_router(auth_router.router)