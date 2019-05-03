import re
import calendar
import collections
from datetime import datetime
import urllib.request
import matplotlib.pyplot as plt
import json
from pymystem3 import Mystem
from matplotlib import style


m = Mystem()
token = 'd63b2b0ad63b2b0ad63b2b0a71d652c7fddd63bd63b2b0a8af7647e20f6450ba2c6234a'
cities = []
unis = []


def to_file(text, file_name):
    with open(r"C:\Users\Николас Алва\Desktop\vkapi_practice\%s" % file_name, "w", encoding="utf-8") as f:
        f.write(text)


def freq(text):
    frq = collections.Counter(text).most_common(20)
    frq = dict(frq)
    frq = {c: frq[c] for c in frq if frq[c] > 0}
    return frq


def clean(text):
    text2 = re.sub("[^а-яА-Я ]", " ", text)
    return text2


def draw_graf_bar(x, y, title, x_name, y_name, col):
    style.use('ggplot')
    plt.title(title)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    plt.xticks(rotation=90)
    plt.bar(x, y, color=col)
    plt.show()
    # plt.savefig('{}.png'.format(title), dpi=100)


def draw_graf_plot(x, y, title, x_name, y_name, col):
    style.use('ggplot')
    plt.title(title)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    plt.plot(x, y, color=col)
    plt.show()
    # plt.savefig('{}.png'.format(title), dpi=100)


def lemm(text):
    text = m.lemmatize(text)
    return text


def user_info(users):
    info = {'city': '', 'uni': ''}
    for user in users:
        try:
            req = urllib.request.Request(
                'https://api.vk.com/method/users.get?v=5.92&access_token=%s'
                '&user_ids={}&fields=city,education'.format(str(user)) % token)
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            data = json.loads(result)
            # print(data)
            if 'city' not in (data['response'][0]):
                continue
            if 'university_name' not in (data['response'][0]):
                continue
            # print(data['response'][0]['city']['title'])
            # print(data['response'][0]['university_name'])
            city = {'city': data['response'][0]['city']['title']}
            uni = {'uni': data['response'][0]['university_name']}
            global cities
            global unis
            cities.append(data['response'][0]['city']['title'])
            unis.append(data['response'][0]['university_name'])
            info.update(city)
            info.update(uni)
            # print(info)
        except:
            pass
    return info


def main():
    texts = []
    offset = [0, 100]
    offset2 = [0, 100, 200]
    posts_d = {}
    comments_d = {}
    owner_id = '-25557243'
    # lens = []
    # users = []
    # получаю тексты постов
    for off in offset:
        req = urllib.request.Request(
            'https://api.vk.com/method/wall.get?owner_id=%s&offset=%s&count=100&v=5.92&access_token=%s' % (owner_id, off,
                                                                                                         token))
        response = urllib.request.urlopen(req)
        result = response.read().decode("utf-8")
        posts = json.loads(result)
        for n in range(len(posts['response']['items'])):
            print('processing...')
            # print(posts['response']['items'][n])
            post_date = posts['response']['items'][n]['date']
            post_date = datetime.fromtimestamp(post_date).strftime('%Y-%m-%d %H:%M:%S')
            datetime_object = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
            week = {'week': calendar.day_name[datetime.weekday(datetime_object)]}
            hour = {'hour': datetime_object.hour}
            text = {'text': posts['response']['items'][n]['text']}
            length = {'length': len(posts['response']['items'][n]['text'].split())}
            post_id = posts['response']['items'][n]['id']
            diction = {post_id: [text, week, hour, length]}
            posts_d.update(diction)
            texts.append(text['text'])

            # теперь выкачиваю комментарии к посту
            for off2 in offset2:
                req = urllib.request.Request(
                    'https://api.vk.com/method/wall.getComments?owner_id=%s&post_id=%s&offset=%s&count=100&v=5.92'
                    '&access_token=%s' % (owner_id, post_id, off2, token))
                response = urllib.request.urlopen(req)
                result = response.read().decode("utf-8")
                comments = json.loads(result)
                for i in range(len(comments['response']['items'])):
                    if 'text' in comments['response']['items'][i]:
                        # print(comments['response']['items'][i]['text'])
                        texts.append(comments['response']['items'][i]['text'])
                        if i > 10:
                            continue
                        # print(comments['response']['items'][i])
                        user_id = {'user_id': comments['response']['items'][i]['from_id']}
                        # print(comments['response']['items'][i]['from_id'])
                        com_text = {'text': comments['response']['items'][i]['text']}
                        id_post = {'post_id': post_id}
                        com_len = {'length': len(comments['response']['items'][i]['text'].split())}
                        us = [user_id['user_id']]
                        info = user_info(us)
                        # print(info)
                        if info is not None:
                            diction = {comments['response']['items'][i]['id']: [com_text, id_post, com_len,
                                                                                info]}
                            comments_d.update(diction)

    # print(posts_d)
    # print(comments_d)
    # print(cities)
    # print(unis)

    ave = 0
    counter = 0
    graf1 = {}
    graf1_sorted = {}
    for key, value in posts_d.items():
        x = value[3]['length']
        for key1, value1 in comments_d.items():
            if key == value1[1]['post_id']:
                ave = + value1[2]['length']
                counter = + 1
        y = round(ave/counter)
        diction = {x: y}
        graf1.update(diction)

    for key in sorted(graf1):
        j = {key: graf1[key]}
        graf1_sorted.update(j)

    draw_graf_bar(graf1_sorted.values(), graf1_sorted.keys(), 'средняя длина комментария в зависимости от длины поста',
                  "средняя длина комментария", "Длина поста", "g")

    graf2 = {}
    ave_week = 0
    for day in calendar.day_name:
        for key, value in posts_d.items():
            if day == value[1]['week']:
                counter = + 1
                ave_week = + value[3]['length']
        dict1 = {day: ave_week/counter}
        graf2.update(dict1)

    draw_graf_plot(graf2.keys(), graf2.values(), "средняя длина поста в зависимости от дня недели", "день недели",
                   "средняя длина поста", "y")

    graf3 = {}
    ave_hour = 0
    for hour in range(24):
        for key, value in posts_d.items():
            if hour == value[2]['hour']:
                counter = + 1
                ave_hour = + value[3]['length']
        dict1 = {hour: round(ave_hour/counter)}
        graf3.update(dict1)
    # print(graf3)
    draw_graf_plot(graf3.keys(), graf3.values(), "средняя длина поста в зависимости от часа публикации", "час",
                   "средняя длина поста", "r")

    texts_str = ' '.join(texts).lower()
    # print(texts_str)
    text_clean = clean(texts_str)
    # print(text_clean)
    to_file(text_clean, 'row_text.txt')
    text_lemm = lemm(text_clean)
    to_file(''.join(text_lemm), 'text_lemmatized.txt')

    nonlem_freq = freq(text_clean.split())
    print("ЧАСТОТНЫЙ СЛОВАРЬ ПО НЕЛЕММАТИЗИРОВАННОМУ КОРПУСУ")
    print(nonlem_freq)
    draw_graf_bar(nonlem_freq.keys(), nonlem_freq.values(), "частотность без лемматизации", "слова", "частота", "r")

    lemm_freq = freq(text_lemm)
    # убираю пробелы из частотного словаря
    lemm_freq = {i: lemm_freq[i] for i in lemm_freq if i != ' ' and i != '  ' and i != '   ' and i != '    '
                 and i != '      ' and i != '     ' and i != '          '}
    print("ЧАСТОТНЫЙ СЛОВАРЬ ПО ЛЕММАТИЗИРОВАННОМУ КОРПУСУ")
    print(lemm_freq)
    draw_graf_bar(lemm_freq.keys(), lemm_freq.values(), "частотность с лемматизацией", "слова", "частота", "m")

    # формирую корпуса с дополнительной информацией в формате json
    to_file(json.dumps(posts_d), "корпус постов.txt")
    to_file(json.dumps(comments_d), "корпус комментариев.txt")
    # print(comments_d)

    graf4 = {}
    ave_city = 0
    for city in cities:
        for key, value in comments_d.items():
            if 'city' in value[3]:
                if city == value[3]['city']:
                    counter = + 1
                    ave_city = + value[2]['length']
        dict1 = {city: round(ave_city / counter)}
        graf4.update(dict1)

    draw_graf_bar(graf4.keys(), graf4.values(), "средняя длина комментария в зависимости от города", "город",
                   "средняя длина", "k")

    # print(comments_d)
    graf5 = {}
    ave_uni = 0
    for uni in unis:
        for key, value in comments_d.items():
            if 'uni' in value[3]:
                if uni == value[3]['uni']:
                    counter = + 1
                    ave_uni = + value[2]['length']
        dict1 = {uni: round(ave_uni / counter)}
        graf5.update(dict1)
    # print(graf5)
    draw_graf_bar(graf5.keys(), graf5.values(), "средняя длина комментария в зависимости от университета", "университет",
                  "средняя длина", "y")


if __name__ == '__main__':
    main()

