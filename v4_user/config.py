from pydantic import BaseSettings

class Settings(BaseSettings):
    database_host:str
    database_post:str
    database_username:str
    database_password:str
    database_name:str
    server_key:str
    algorithm:str
    expiration_minutes:int

    class Config:
        env_file=".env"

settings=Settings()        
