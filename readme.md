# Генератор анекдотов
Ансамбль моделей Qwen2.5-1.5B-Instruct + DistilBertForSequenceClassification для генерации и оценки анекдотов (шуток) вместе с тренировочными датасетами и весами соответствующих моделей.

## Использование
Генерация анекдота по его затравке:
```
python get_anecdote.py
``` 
**inference.ipynb** - ноутбук с примером инференса, если скрипт не нравится 

**bert_train.ipynb** - ноутбук с примером обучения Берта.

**qwen_train.ipynb** - ноутбук с примером обучения Квена.

**parser.py** - парсер, использовавшийся при парсинге **anekdot.ru**.

## Environment

**requirements.txt** - pip.

**requirements_if_you_cant_use_python313.txt** -- pip если вы тоже не можете в датасфере пользоваться питоном новее 3.10.

**jokes.yml** -- conda.

**jokes_if_you_cant_use_python313.yml** - conda если вы тоже не можете в датасфере пользоваться питоном новее 3.10.