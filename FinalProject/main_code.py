import re
import urllib.request
import matplotlib.pyplot as plt
import json
from pymystem3 import Mystem
from matplotlib import style
import pylab
import random
import numpy as np
from pandas import DataFrame

m = Mystem()
token = '20e828f720e828f720e828f7a12081c400220e820e828f77de1252ae36d5c035ee4deac'
cities = []
unis = []
colours = ['g', 'r', 'b', 'y']

owner_ids = {'-32038': "Буквоед", '-23065467':"Книги. Издательство АСТ", '-23482323': "ЛитРес Книги", '-24831014': 'Лабиринт'}
words_list = {"автор":0, "бестселлер":0, "скидка":0, "сюжет":0, "герой":0, "детектив":0, "фантастика":0, "роман":0,
              "новинка":0, "розыгрыш":0, "классика":0, "премия":0, "сказка":0}


def analise(text, title):
    words_list2 = words_list
    for word in text:
        if word in words_list.keys():
            words_list2[word] += 1
    print(words_list2)
    draw_graf_bar(words_list2.keys(), words_list2.values(), title, "слова", "частотность", random.choice(colours))
    return words_list2

def clean(text):
    text2 = re.sub("[^а-яА-Я ]", " ", text)
    return text2.lower()


def lemm(text):
    text = m.lemmatize(text)
    return text


def draw_graf_bar(x, y, title, x_name, y_name, col):
    style.use('ggplot')
    plt.title(title)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    plt.xticks(rotation=90)
    plt.bar(x, y, color=col)
    plt.savefig('{}.png'.format(title), dpi=100)
    plt.show()



def draw_graf_overall(data):
    df = DataFrame({
        "слова": ["автор", "бестселлер", "скидка", "сюжет", "герой", "детектив", "фантастика",
                  'роман', 'новинка', 'розыгрыш','классика', 'премия', 'сказка'],
        "Буквоед": data[0],
        "Книги. Издательство АСТ": data[1],
        "ЛитРес Книги": data[2],
        "Лабиринт": data[3]
    })
    df.set_index('слова', inplace=True)
    print(df)
    df.plot(kind='bar')
    plt.savefig('{}.png'.format("сводная"), dpi=100)
    plt.show()


def main():
    text = ''
    info_overall = []
    offset = [0, 100, 200]
    for owner_id in owner_ids:
        print(owner_id)
        for off in offset:
            req = urllib.request.Request(
                'https://api.vk.com/method/wall.get?owner_id=%s&offset=%s&count=100&v=5.92&access_token=%s' % (owner_id, off,
                                                                                                             token))
            response = urllib.request.urlopen(req)
            result = response.read().decode("utf-8")
            posts = json.loads(result)
            for n in range(len(posts['response']['items'])):
                print('processing...')
                text = text + " " + posts['response']['items'][n]['text']
        data = analise(lemm(clean(text)), owner_ids[owner_id])
        print(data)
        info_overall.append(list(data.values()))

    # print(info_overall)
    draw_graf_overall(info_overall)


if __name__ == '__main__':
    main()