# Генератор демотиваторов
Ансамбль моделей Qwen2.5-1.5B-Instruct + DistilBertForSequenceClassification + Stable-diffusion-v1-5 для генерации и оценки анекдотов (шуток) и генерации картинок к ним вместе с тренировочными датасетами и весами соответствующих моделей.

## Клонирование репозитория
Перед клонированием убедитесь, что у вас установлен git-lfs!

## Использование
Запуск сервера:
```
python app/main.py
```
Генерация анекдота по его затравке:
```
python /experiments/get_anecdote.py
``` 
**/experiments/inference.ipynb** - ноутбук с примером инференса, если скрипт не нравится.

**/experiments/bert_train.ipynb** - ноутбук с примером обучения Берта.

**/experiments/qwen_train.ipynb** - ноутбук с примером обучения Квена.

**/parser/parser.py** - парсер, использовавшийся при парсинге **anekdot.ru**.

**data/** -- директория с датасетами.

## Environment

**requirements.txt** - pip зависимости для инференса и деплоя.

**jokes.yml** -- conda окружение для обучения.

