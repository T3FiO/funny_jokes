from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, DistilBertTokenizer, DistilBertForSequenceClassification
import os

from get_anecdote import get_anecdote

app = FastAPI()

qwen_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
# checkpath = os.path.join('qwen2.5-lora-jokes', 'v2.0', 'checkpoint-764_scoutie' ) # scoutie dataset
checkpath = os.path.join('../qwen2.5-lora-jokes', 'v2.0', 'checkpoint-2906_parsed') # parsed dataset
qwen_model = AutoModelForCausalLM.from_pretrained(checkpath, trust_remote_code=True)
qwen_model.eval()

bert_model = DistilBertForSequenceClassification.from_pretrained('funny_jokes_classifier.model')
bert_tokenizer = DistilBertTokenizer.from_pretrained('funny_jokes_classifier.tokenizer')


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

@app.post("/process")
async def process_text(input_data: TextInput):
    # Here you can add your text processing logic
    # For now, we'll just return a simple response
    anecdote = get_anecdote(qwen_model, qwen_tokenizer, bert_model, bert_tokenizer, input_data.text, n=5, top_1=True)
    return {"response": f"Полученный анекдот: {anecdote}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)