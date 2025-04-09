---
task_categories:
- text-classification
- feature-extraction
- text-generation
- zero-shot-classification
- text2text-generation
language:
- ru
tags:
- russia
- jokes
- vectors
- sentiment
- ner
- clusterisation
pretty_name: Russian Jokes
size_categories:
- 10K<n<100K
---

## Description in English:
  The dataset is collected from Russian-language Telegram channels with jokes and anecdotes,\
The dataset was collected and tagged automatically using the data collection and tagging service [Scoutie](https://scoutie.ru/).\
Try Scoutie and collect the same or another dataset using [link](https://scoutie.ru/) for FREE.

## Dataset fields:
  **taskId** - task identifier in the Scouti service.\
  **text** - main text.\
  **url** - link to the publication.\
  **sourceLink** - link to Telegram.\
  **subSourceLink** - link to the channel.\
  **views** - text views.\
  **likes** - for this dataset, an empty field (meaning the number of emotions).\
  **createTime** - publication date in unix time format.\
  **createTime** - publication collection date in unix time format.\
  **clusterId** - cluster id.\
  **vector** - text embedding (its vector representation).\
  **ners** - array of identified named entities, where lemma is a lemmatized representation of a word, and label is the name of a tag, start_pos is the starting position of an entity in the text, end_pos is the ending position of an entity in the text.\
  **sentiment** - emotional coloring of the text: POSITIVE, NEGATIVE, NEUTRAL.\
  **language** - text language RUS, ENG.\
  **spam** - text classification as advertising or not NOT_SPAM - no advertising, otherwise SPAM - the text is marked as advertising.\
  **length** - number of tokens in the text (words).\
  **markedUp** - means that the text is marked or not within the framework of the Skauti service, takes the value true or false.

## Описание на русском языке:
  Датасет собран из русскоязычных Telegram  каналов c шутками и анекдотами,\
Датасет был собран и размечен автоматически с помощью сервиса сбора и разметки данных [Скаути](https://scoutie.ru/).\
Попробуй Скаути и собери такой же или другой датасет по [ссылке](https://scoutie.ru/) БЕСПЛАТНО.

## Поля датасета:
  **taskId** - идентификатор задачи в сервисе Скаути.\
  **text**  - основной текст.\
  **url** - ссылка на публикацию.\
  **sourceLink** -  ссылка на Telegram.\
  **subSourceLink** - ссылка на канал.\
  **views** - просмотры текста.\
  **likes** - для данного датасета пустое поле (означающее количество эмоций).\
  **createTime** - дата публикации в формате unix time.\
  **createTime** - дата сбора публикации в формате unix time.\
  **clusterId** - id кластера.\
  **vector** -  embedding текста (его векторное представление).\
  **ners** - массив выявленных именованных сущностей, где lemma - лемматизированное представление слова, а label это название тега, start_pos - начальная позиция сущности в тексте, end_pos - конечная позиция сущности в тексте.\
  **sentiment** - эмоциональный окрас текста: POSITIVE, NEGATIVE, NEUTRAL.\
  **language** - язык текста RUS, ENG.\
  **spam** - классификация текста, как рекламный или нет NOT_SPAM - нет рекламы, иначе SPAM - текст помечен, как рекламный.\
  **length** -  количество токенов в тексте (слов).\
  **markedUp** - означает, что текст размечен или нет в рамках сервиса Скаути принимает значение true или false.