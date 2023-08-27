import logging
import os
import uvicorn
import pandas as pd

from fastapi import FastAPI

from app.src.models import AnswerRequest, AnswerResponse
from app.src.search import EmbeddingSimilaritySearch

logging.basicConfig(level=logging.INFO)

SEARCH_KEY = os.getenv('SEARCH_KEY')
INIT_QA_DOCUMENTS = os.getenv('INIT_QA_DOCUMENTS')
MODEL_PATH = os.getenv('EMBEDDING_MODEL_PATH')
TOP_K = int(os.getenv('DEFAULT_TOP_K'))
ANSWER_THRESHOLD = float(os.getenv('ANSWER_THRESHOLD'))

app = FastAPI()
search = EmbeddingSimilaritySearch(model_name_or_path=MODEL_PATH, answer_threshold=ANSWER_THRESHOLD)


def populate_search(qa_df_path: str):
    qa_df = pd.read_csv(qa_df_path)
    search.populate(qa_df.to_dict('records'), search_key=SEARCH_KEY)


@app.post("/answer")
async def read_root(request: AnswerRequest) -> AnswerResponse:
    query = request.question
    candidates = search.search(query, top_k=TOP_K)
    return AnswerResponse(candidates=candidates)


populate_search(qa_df_path=INIT_QA_DOCUMENTS)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
