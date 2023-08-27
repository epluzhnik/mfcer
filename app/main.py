import logging
import os
import re

import fastapi
import pandas as pd
import uvicorn
from fastapi import FastAPI

from app.src.models import AnswerRequest, AnswerResponse, QARequest, AnswerFrequency
from app.src.search import EmbeddingSimilaritySearch

app = FastAPI()

logging.basicConfig(level=logging.INFO)

SEARCH_KEY = os.getenv('SEARCH_KEY')
INIT_QA_DOCUMENTS = os.getenv('INIT_QA_DOCUMENTS')
MODEL_PATH = os.getenv('EMBEDDING_MODEL_PATH')
TOP_K = int(os.getenv('DEFAULT_TOP_K'))
ANSWER_THRESHOLD = float(os.getenv('ANSWER_THRESHOLD'))

search = EmbeddingSimilaritySearch(model_name_or_path=MODEL_PATH, answer_threshold=ANSWER_THRESHOLD)

ru_mask = r'[^а-яА-ЯёЁ0-9]'


def clean_text_question(text: str) -> str:
    temp = re.sub(ru_mask, ' ', text)
    return " ".join(temp.split())


def populate_search(qa_df_path: str):
    qa_df = pd.read_csv(qa_df_path)
    search.populate(qa_df.to_dict('records'), search_key=SEARCH_KEY)


@app.post("/answer")
async def read_root(request: AnswerRequest) -> AnswerResponse:
    query = request.question
    query = query.lower()
    query = clean_text_question(query)
    candidates = search.search(query, top_k=TOP_K)
    return AnswerResponse(candidates=candidates)


populate_search(qa_df_path=INIT_QA_DOCUMENTS)

metrics: dict[str, AnswerFrequency] = {}


@app.post("/metrics")
async def post_metrics(request: QARequest) -> fastapi.Response:
    if request.question in metrics.keys():
        metrics[request.question].frequency += 1
    else:
        metrics[request.question] = AnswerFrequency(1, request.answer, request.question)

    return fastapi.Response(status_code=200)


@app.post("/metrics/answer")
async def post_metrics(request: AnswerRequest) -> fastapi.Response:
    if request.question in metrics:
        return metrics[request.question].answer
    else:
        return fastapi.Response(status_code=404)


@app.get("/metrics")
async def get_metrics() -> [AnswerFrequency]:
    questions = sorted(metrics.values(), key=lambda item: item.frequency, reverse=True)

    return questions[:5]


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
