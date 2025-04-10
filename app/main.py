from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from model import main_func
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
)
import os
from diffusers import StableDiffusionPipeline
import torch


@asynccontextmanager
async def lifespan(app: FastAPI):

    checkpath = os.path.join(
        "../qwen2.5-lora-jokes", "v2.0", "checkpoint-2906_parsed"
    )  # parsed dataset
    app.state.qwen_tokenizer = AutoTokenizer.from_pretrained(
        "Qwen/Qwen2.5-1.5B-Instruct"
    )
    app.state.qwen_model = PeftModel.from_pretrained(
        AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct"), checkpath
    )
    app.state.qwen_model.eval()

    app.state.bert_model = DistilBertForSequenceClassification.from_pretrained(
        "../funny_jokes_classifier.model"
    )
    app.state.bert_tokenizer = DistilBertTokenizer.from_pretrained(
        "../funny_jokes_classifier.tokenizer"
    )

    app.state.dif_model = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32
    )

    print("Models and tokenizers initialized.")
    yield

    # Освобождение ресурсов (если необходимо)
    del app.state.qwen_model
    del app.state.qwen_tokenizer
    del app.state.bert_model
    del app.state.bert_tokenizer
    del app.state.dif_model
    print("Models and tokenizers released.")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_main_page(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})


class TextData(BaseModel):
    text: str


@app.post("/process")
async def receive_text(data: TextData):
    qwen_model = app.state.qwen_model
    qwen_tokenizer = app.state.qwen_tokenizer
    bert_model = app.state.bert_model
    bert_tokenizer = app.state.bert_tokenizer
    dif_model = app.state.dif_model
    img_url, text = main_func(
        qwen_model,
        qwen_tokenizer,
        bert_model,
        bert_tokenizer,
        dif_model,
        data.text,
        n=5,
        top_1=True,
    )
    return {"text": text, "img_url": img_url}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
