from PIL import Image, ImageOps
import warnings

warnings.filterwarnings("ignore")
import torch
import numpy as np


MAX_LEN = 128


def predict_funny_score(model, joke, tokenizer):
    model.to("cpu")
    # Токенизация
    encoded_joke = tokenizer.encode_plus(
        joke,
        max_length=MAX_LEN,
        add_special_tokens=True,
        return_token_type_ids=False,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_tensors="pt",
    )

    input_ids = encoded_joke["input_ids"].to("cpu")
    attention_mask = encoded_joke["attention_mask"].to("cpu")

    # Предсказание
    with torch.no_grad():
        output = model(input_ids, attention_mask)

    # Получаем сырое предсказание
    prediction = output.logits.squeeze()

    return 1 / (1 + np.exp(-prediction))


def get_anecdote(
    qwen_model, qwen_tokenizer, bert_model, bert_tokenizer, prompt, n=5, top_1=True
):
    """
    Генерирует по промпту n ответов и выбирает из них самый смешной, если top_1 == True,

    Выдаёт list всех ответов иначе.
    """
    messages = [
        {
            "role": "system",
            "content": "Ты генератор шуток, отвечай только с помощью анекдотов.",
        },
        {"role": "user", "content": "Заходит бесконечное количество математиков в бар"},
        {
            "role": "assistant",
            "content": "Бесконечное число математиков заходит в бар. Первый говорит: «Мне кружку пива!». Второй говорит: «Мне половину кружки пива!» Третий говорит: «Мне четверть кружки пива!» Четвертый говорит: «Мне 1/8 кружки пива!» Бармен:– Да знаю я вас – вам две кружки на всех!",
        },
        {"role": "user", "content": prompt},
    ]
    text = qwen_tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = qwen_tokenizer([text], return_tensors="pt").to(qwen_model.device)

    generated_ids = qwen_model.generate(
        **model_inputs,
        max_new_tokens=256,
        num_return_sequences=n,  # Количество ответов
    )

    anecdotes = [
        prompt
        + "\n"
        + qwen_tokenizer.batch_decode(
            [
                output_ids[len(input_ids) :]
                for input_ids, output_ids in zip(
                    model_inputs.input_ids, [generated_ids[i]]
                )
            ],
            skip_special_tokens=True,
        )[0]
        for i in range(len(generated_ids))
    ]
    # Загрузка модели

    max = 0
    i_max = 0
    if top_1:
        for i, anecdote in enumerate(anecdotes):
            score = predict_funny_score(bert_model, anecdote, bert_tokenizer)
            if score > max:
                max = score
                i_max = i
        return anecdotes[i_max]
    else:
        return anecdotes


def get_image(model, prompt):
    image = model(prompt, height=128, width=128).images[0]
    image = image.resize((384, 384))
    image = ImageOps.expand(image, border=2, fill="white")
    image.save("images/test.png")
    return "images/test.png"


def main_func(
    qwen_model,
    qwen_tokenizer,
    bert_model,
    bert_tokenizer,
    dif_model,
    prompt,
    n=5,
    top_1=True,
):
    anec = get_anecdote(
        qwen_model, qwen_tokenizer, bert_model, bert_tokenizer, prompt, n=n, top_1=top_1
    )
    image_path = get_image(dif_model, anec)
    return image_path, anec
