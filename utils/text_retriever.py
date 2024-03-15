import hnswlib
import numpy as np
import os
from typing import List, Dict, Tuple

class TextRetriever:
    # 每个user有自己的text retriever
    def __init__(self, knn_path:str, text2vec_model, embedding_dim=768, max_num=20000):
        self.embedding_dim = embedding_dim
        self.knn = hnswlib.Index(space='l2', dim=self.embedding_dim)
        self.knn_path = knn_path
        self.knn.init_index(max_elements = max_num, ef_construction = 200, M = 16)

        if os.path.exists(knn_path):
            # exists, load
            self.knn.load_index(knn_path)

        self.t2v_model = text2vec_model

    def enroll(self, texts: List[str], ids:List[int]): 
        emb = self.t2v_model.encode(texts)
        self.knn.add_items(emb, ids)

    def delete(self, ids: List[int]):
        for id in ids:
            self.knn.mark_deleted(id)
    
    def save(self):
        self.knn.save_index(self.knn_path)
    
    def retrieve(self, query: str, max_items=5, score_threshold=0.3):
        emb = self.t2v_model.encode([query])
        ids, distances = self.knn.knn_query(emb, k=max_items)
        #res = []
        #for i in range(len(ids)):
            # if distances[0][i] > score_threshold:
        #    res.append(ids[0][i])
        return ids[0].tolist()
    


