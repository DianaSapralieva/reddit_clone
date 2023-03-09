from pydantic import BaseSettings

class Settigs(BaseSettings):
    database_host:str
    database_port:str
    database_username:str
    database_password:str
    database_name:str
    database_key:str
    algorithm:str
    exparation_minutes:int

    class Config:
        env_file=".env"

settings=Settigs()        
