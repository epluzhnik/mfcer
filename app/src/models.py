from pydantic import BaseModel


class AnswerRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    candidates: list[dict]
