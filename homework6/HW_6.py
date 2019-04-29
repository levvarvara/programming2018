import re
import calendar
from datetime import datetime
# from datetime import date
import urllib.request
import matplotlib.pyplot as plt
import json
from pymystem3 import Mystem
from string import punctuation


m = Mystem()
token = '2578038a2578038a2578038a3d2511ef7d225782578038a79bf393a4a54468e4eb649d2'


def clean(text):
    text2 = re.sub("[^а-яА-Я ]", "", text)
    return text2


def draw_graf(x, y, title, x_name, y_name, col):
    plt.title(title)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    plt.bar(x, y, color=col)
    plt.show()

def lemm(text):
    text = m.lemmatize(text)
    return text

def user_info(users):
    info = {}
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
            info.update(city)
            info.update(uni)
            return info
        except:
            pass


def main():
    texts = []
    offset = [0, 100]
    offset2 = [0, 100, 200]
    posts_d = {}
    comments_d = {}
    owner_id = '-25557243'
    # users = []
    # получаем тексты постов
    for off in offset:
        req = urllib.request.Request(
            'https://api.vk.com/method/wall.get?owner_id=%s&offset=%s&count=100&v=5.92&access_token=%s' % (owner_id, off, token))
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

            # теперь выкачиваем комментарии к посту
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
                        diction = {comments['response']['items'][i]['id']: [com_text, id_post, com_len, info]}
                        comments_d.update(diction)
    print(posts_d)
    print(comments_d)

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
    print(graf1_sorted)
    draw_graf(graf1_sorted.values(), graf1_sorted.keys(), 'средняя длина комментария в зависимости от длины поста',
              "Средняя длина комментария", "Длина поста", "g")

    graf2 = {}
    for day in calendar.day_name:
        for key, value in posts_d.items():
            if day == value[1]['week']:
                counter = + 1
                ave_week = + value[3]['length']
        dict1 = {day: ave_week/counter}
        graf2.update(dict1)

    draw_graf(graf2.keys(), graf2.values(), "средняя длина поста в зависимости от дня недели", "день недели",
              "средняя длина поста", "y")

    graf3 = {}
    for hour in range(24):
        for key, value in posts_d.items():
            if hour == value[2]['hour']:
                counter = + 1
                ave_hour = + value[3]['length']
        dict1 = {hour: round(ave_hour/counter)}
        graf3.update(dict1)
    print(graf3)
    draw_graf(graf3.keys(), graf3.values(), "средняя длина поста в зависимости от часа публикации", "час",
              "средняя длина поста", "r")

    text_clean = clean(text)
    print(text_clean)
    lem_text = lemm(text_clean)
    print(lem_text)


if __name__ == '__main__':
    main()
