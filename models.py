from pydantic import BaseModel

class NPC(BaseModel):
    name: str
    backstory: str
    image_link: str

class Location(BaseModel):
    name: str
    description: str
    image_link: str

class User(BaseModel):
    name: str
    backstory: str
    image_link: str