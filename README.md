1. Deplpoy InterLM2 to 127.0.0.1:9527/api

2. Download models and move into models/

   models/whisper https://huggingface.co/openai/whisper-large-v3

   models/sentence_model https://huggingface.co/shibing624/text2vec-base-chinese

   models/chinese-clip-vit-huge-patch14 https://huggingface.co/OFA-Sys/chinese-clip-vit-huge-patch14

4. Install requirements.txt

5. Start backend by running
   ```
   cd apis/
   uvicorn main_app:app --reload 
   ```

7. Go to http://localhost/docs
