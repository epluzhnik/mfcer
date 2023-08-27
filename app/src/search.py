import logging
from copy import deepcopy

import torch
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)


class SearchCandidate(BaseModel):
    similarity: float
    candidate: dict


class EmbeddingSimilaritySearch:
    def __init__(self, model_name_or_path: str, answer_threshold: float):
        logger.info('Loading model...')

        self._model = SentenceTransformer(model_name_or_path)
        self._answer_threshold = answer_threshold

        self._embeddings = None
        self._data = None

    def populate(self, data: list[dict], search_key: str):
        logger.info('Populating search...')

        search_keys = [item[search_key] for item in data]
        self._embeddings = self._model.encode(search_keys)
        self._data = deepcopy(data)

    def search(self, query: str, top_k: int = 5) -> list[SearchCandidate]:
        if self._data is None:
            logger.warning('Cannot search - no populated data')
            return []

        query_embedding = self._model.encode(query)

        cosine_scores = util.pytorch_cos_sim(query_embedding, self._embeddings)[0]
        top_results = torch.topk(cosine_scores, k=top_k)  # tuple[score, index]

        return [
            SearchCandidate(similarity=similarity, candidate=self._data[index]) for similarity, index in
            zip(*top_results) if similarity > self._answer_threshold
        ]
