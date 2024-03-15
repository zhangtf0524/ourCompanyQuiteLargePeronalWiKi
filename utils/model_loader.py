import whisper
import torch
import numpy as np
import os
from text2vec import SentenceModel
from similarities import ClipSimilarity


asr_model_path = './models/whisper/large-v3.pt'
img_LM_path = './models/internlm-xcomposer2-7b-4bit'
t2v_model_path = './models/sentence_model'
clip_model_path = './models/chinese-clip-vit-base-patch16'

# 文本embedding模型
text2vec_model = SentenceModel(t2v_model_path)

# 语音转文字模型
asr_model = whisper.load_model(asr_model_path)

# 图片-文本匹配模型
clip_model = ClipSimilarity(model_name_or_path=clip_model_path)
