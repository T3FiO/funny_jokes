from bs4 import BeautifulSoup as BS
import requests as req
import csv
import os

def get_page(url):
    page = req.get(url)
    if (page.status_code != 200):
        print("\t", url)
        print("\tProblem ? page_status: ", page.status_code)
        return None
    page.encoding = 'utf-8'
    page_BS = BS(page.text, "html.parser")
    return page_BS 

def find_all_jokes_as_tags(page):
    jokes_tags = page.find_all(attrs={"class": "topicbox", "data-t": "j"})
    return jokes_tags

def get_text_joke(joke_tag):
    div = joke_tag.find(class_ = "text")
    text = div.get_text(separator=' ', strip=True)
    clean_text = text.encode('utf-8').decode('utf-8')  # Для уверенности
    return clean_text

def parse_rate(joke_tag):
    div = joke_tag.find(class_ = "rates")
    if (div == None):
        return None
    return div['data-r'].split(';')[0]

def get_year():
    year = 2025
    while (year >= 1995):
        yield year
        year -= 1

def get_week(start_week=52, end_week=1):
    week = start_week
    while (week >= end_week):
        yield week
        week -= 1

def get_extra_pages(page):
    div = page.find(class_ = "pageslist")
    if (div == None):
        return None

    max_page = int(div.find_all("a")[-2].string)
    pages = []
    for i in range(1, max_page + 1):
        pages.append(i)

    return pages

if (__name__ == "__main__"):
    base_url = "https://www.anekdot.ru/release/anekdot/week"
    filename = 'data_jokes.csv' 
    write_header = not os.path.exists(filename) or os.stat(filename).st_size == 0

    data = []
    for year in get_year():
        start_week = 52
        end_week = 1
        if year == 2025:
            start_week = 14
        if year == 1995:
            end_week = 46

        for week in get_week(start_week, end_week):
            url  = base_url + '/' + str(year) + '-' + str(week)
            page = get_page(url)
            extra_pages_gen = get_extra_pages(page)
            if (extra_pages_gen == None):
                print("INFO: Parsing ", url + '/' + str(page))

                jokes_tag = find_all_jokes_as_tags(page)
                for joke_tag in jokes_tag:
                    rate = parse_rate(joke_tag)
                    if (rate == None):
                        continue
                    if (int(rate) < 5):
                        continue
                    joke = get_text_joke(joke_tag)
                    data.append([rate, joke])

            else:
                for extra_page in extra_pages_gen:
                    print("INFO: Parsing ", url + '/' + str(extra_page))
                    extra_page = get_page(url + '/' + str(extra_page))

                    jokes_tag = find_all_jokes_as_tags(extra_page)
                    for joke_tag in jokes_tag:
                        rate = parse_rate(joke_tag)
                        if (rate == None):
                            continue
                        joke = get_text_joke(joke_tag)
                        data.append([rate, joke])

            with open('data_jokes.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if write_header:
                    writer.writerow(['rate', 'joke'])
                    write_header = False
                writer.writerows(data)
            data = []
