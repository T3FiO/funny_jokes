import warnings
warnings.filterwarnings("ignore")
from transformers import AutoModelForCausalLM, AutoTokenizer, BertForSequenceClassification, BertTokenizer
from peft import PeftModel
import torch
import numpy as np
import os



def get_anecdote(prompt, n =5):
    '''
    Генерирует по промпту n ответов и выбирает из них самый смешной
    '''
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # checkpath = os.path.join('qwen2.5-lora-jokes', 'v2.0', 'checkpoint-764_scoutie' ) # scoutie dataset
    checkpath = os.path.join('qwen2.5-lora-jokes', 'v2.0', 'checkpoint-2906_parsed' ) # parsed dataset
    # checkpath = 'qwen2.5-lora-jokes/v2.0/checkpoint-764'
    model = AutoModelForCausalLM.from_pretrained(checkpath, trust_remote_code=True)
    # model = PeftModel.from_pretrained(base_model, checkpath)
    # model = model.merge_and_unload(Пе)
    model.eval()
    messages = [
        {"role": "system", "content": "Ты генератор шуток, отвечай только с помощью анекдотов."},
        {"role": "user", "content": "Заходит бесконечное количество математиков в бар"},
        {"role": "assistant", "content": "Бесконечное число математиков заходит в бар. Первый говорит: «Мне кружку пива!». Второй говорит: «Мне половину кружки пива!» Третий говорит: «Мне четверть кружки пива!» Четвертый говорит: «Мне 1/8 кружки пива!» Бармен:– Да знаю я вас – вам две кружки на всех!"},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=256,
        num_return_sequences = n, # Количество ответов
    )

    anecdotes = [prompt + '\n' + tokenizer.batch_decode([
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, [generated_ids[i]])
        ], skip_special_tokens=True)[0] for i in range(len(generated_ids))]
    # Загрузка модели
    bert = BertForSequenceClassification.from_pretrained('funny_jokes_classifier.model')
    bert_tokenizer = BertTokenizer.from_pretrained('funny_jokes_classifier.tokenizer')
    MAX_LEN= 128
    # Предсказание на новом тексте
    def predict_funny_score(model, joke, tokenizer):
        model.to('cpu')
        # Токенизация
        encoded_joke = tokenizer.encode_plus(
            joke,
            max_length=MAX_LEN,
            add_special_tokens=True,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        input_ids = encoded_joke['input_ids'].to('cpu')
        attention_mask = encoded_joke['attention_mask'].to('cpu')

        # Предсказание
        with torch.no_grad():
            output = model(input_ids, attention_mask)

        # Получаем сырое предсказание
        prediction = output.logits.squeeze()

        return 1 / (1 + np.exp(-prediction))
    max = 0
    i_max = 0
    for i, anecdote in enumerate(anecdotes):
        score = predict_funny_score(bert, anecdote, bert_tokenizer)
        if score > max:
            max = score
            i_max = i
    return anecdotes[i_max]

def main():
    
    prompt = input('Введите начало анекдота:')
    print(get_anecdote(prompt, 2))
if __name__ == '__main__':
    main()