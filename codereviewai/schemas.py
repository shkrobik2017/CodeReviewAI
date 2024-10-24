from pydantic import BaseModel


class ReviewRequest(BaseModel):
    assignment_description: str
    github_repo_url: str
    candidate_level: str


class ResponseSchema(BaseModel):
    files_found: list
    response: str
