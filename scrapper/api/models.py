from pydantic import BaseModel


class UserUrlSubmission(BaseModel):
    id: str
    url: str


class UserAuth(BaseModel):
    name: str
    email: str
    password: str



class Term(BaseModel):
    search_term: str