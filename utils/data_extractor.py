import whisper
from modelscope import AutoTokenizer, AutoModelForCausalLM
from PIL import Image
import torch


class DataExtractor:
    # 全局共享一个信息提取器
    def __init__(self, ocr_model, asr_model):

        self.piece_length = 50
        # load whisper model
        self.asr_model = asr_model # whisper.load_model(self.asr_model_path)
        # load ocr model
        self.ocr_model = ocr_model

    def extract_data(self, file_type, path):
        if file_type == 'image':
            text = self.extract_image_info(path)
            return [text]
        elif file_type == 'audio':
            return self.extract_audio_info(path)
        else:
            return ""
    
    def extract_image_info(self, path):
        result = self.ocr_model.ocr(path, cls=True)
        text = []
        for res in result:
            for line in res:
                text.append(line[-1][0])
        return ','.join(text)

    def extract_audio_info(self, path):
        result = self.asr_model.transcribe(path)
        segments = result["segments"]
        texts = []
        crt = ''
        for seg in segments:
            crt += (seg["text"]+',')
            if len(crt) > self.piece_length + 1:
                texts.append(crt)
                crt = ''
        if len(crt) > 0:
            texts.append(crt)
        return texts
