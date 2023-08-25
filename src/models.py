from pydantic import BaseModel
class AnswerRequest(BaseModel):
    question: str