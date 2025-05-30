# app/abstractive.py
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class AbstractiveSummarizer:
    def __init__(self, model_name='facebook/bart-large-cnn'):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model_name = model_name
        
        if 'bart' in model_name.lower():
            self.summarizer = pipeline('summarization', model=model_name, device=0 if self.device == 'cuda' else -1)
        else:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def summarize(self, text, max_length=130, min_length=30):
        if 'bart' in self.model_name.lower():
            result = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return result[0]['summary_text']
        else:
            inputs = self.tokenizer.encode("summarize: " + text, return_tensors='pt', 
                                         max_length=1024, truncation=True).to(self.device)
            outputs = self.model.generate(inputs, max_length=max_length, min_length=min_length, 
                                        length_penalty=2.0, num_beams=4, early_stopping=True)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)