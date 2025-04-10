from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, DistilBertTokenizer, DistilBertForSequenceClassification
import os

from get_anecdote import get_anecdote

@asynccontextmanager
async def lifespan(app: FastAPI):

    checkpath = os.path.join('../../qwen2.5-lora-jokes', 'v2.0', 'checkpoint-2906_parsed')  # parsed dataset
    app.state.qwen_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
    app.state.qwen_model = PeftModel.from_pretrained(AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct"), checkpath)
    app.state.qwen_model.eval()

    app.state.bert_model = DistilBertForSequenceClassification.from_pretrained('../../funny_jokes_classifier.model')
    app.state.bert_tokenizer = DistilBertTokenizer.from_pretrained('../../funny_jokes_classifier.tokenizer')

    print("Models and tokenizers initialized.")
    yield

    # Освобождение ресурсов (если необходимо)
    del app.state.qwen_model
    del app.state.qwen_tokenizer
    del app.state.bert_model
    del app.state.bert_tokenizer
    print("Models and tokenizers released.")


app = FastAPI(lifespan=lifespan)


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
async def process_text(input_data : TextInput):

    qwen_model = app.state.qwen_model
    qwen_tokenizer = app.state.qwen_tokenizer
    bert_model = app.state.bert_model
    bert_tokenizer = app.state.bert_tokenizer
    anecdote = get_anecdote(qwen_model, qwen_tokenizer, bert_model, bert_tokenizer, input_data.text, n=5, top_1=True)
    return {"response": f"Полученный анекдот: {anecdote}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)