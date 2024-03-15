from similarities import ClipSimilarity
from PIL import Image
from typing import List, Dict, Tuple


class ImageRetriever:
    def __init__(self, image_paths:List[str], clip_model):
        self.image_paths = image_paths
        self.imgs = [Image.open(i) for i in self.image_paths]
        self.clip_model = clip_model
    
    def retrieve(self, query:str, max_items=3, score_threshold=0.35):
        texts = [query]
        sim_scores = self.clip_model.similarity(self.imgs, texts).squeeze().tolist()
        id_scores = sorted([(idx, score) for idx, score in enumerate(sim_scores)], key = lambda x:-x[1]) 
        id_scores_cut = id_scores[:max_items] if len(id_scores) > max_items else id_scores
        res = []
        for one in id_scores_cut:
            if one[1] >= score_threshold:
                res.append(self.image_paths[one[0]])
        return res
    
