from pydantic import BaseModel


class AnswerRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    candidates: list[dict]


class QARequest(BaseModel):
    question: str
    answer: str


class AnswerFrequency:
    def __init__(self, frequency, answer, question):
        self.frequency = frequency
        self.answer = answer
        self.question = question