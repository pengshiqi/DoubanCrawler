# -*- coding: utf-8 -*-
import requests
import time
from pprint import pprint
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


def check_date(date_str, start_str, end_str):
    '''
    判断 date_str 是否在 start_str 和 end_str 之间。
    日期格式: 2017-12-01
    '''

    TIMESTAMP="%Y-%m-%d"
    date = time.mktime(time.strptime(date_str,TIMESTAMP))
    start = time.mktime(time.strptime(start_str,TIMESTAMP))
    end = time.mktime(time.strptime(end_str,TIMESTAMP))

    if (date > end):
        return 2
    elif (start <= date <= end):
        return 1
    else:
        return 0


def get_movie_rate(movie_url):
    '''
    获取某部电影的评分。
    '''
    r = requests.get(movie_url, headers=headers)
    soup = BeautifulSoup(r.text)
    d = soup.select('.rating_num')
    return float(d[0].text.strip())


def get_user_watched_movies(user_id, start_str, end_str):
    '''
    获取我在某一段时间内标记的电影。
    日期格式: 2017-12-01
    '''
    movie_list = []

    i = 0
    till_end = False

    while not till_end:

        url = 'https://movie.douban.com/people/{}/collect?start={}&sort=time&rating=all&filter=all&mode=list'.format(user_id, 30 * i)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text)
        # 提取出电影列表
        d = soup.select('.item')

        # print d[0].a['href']
        # 处理每一个电影
        if (len(d) == 0):
            till_end = True

        for item in d:
            # 判断是否在起始日期之间
            date = item.select('.date')[0].text.strip()
            check_score = check_date(date, start_str, end_str)
            # print(check_score)
            if (check_score == 1):

                movie = {}
                
                movie['name'] = item.a.text.strip()
                print(u'正在处理: {}'.format(movie['name']))
                movie['url'] = item.a['href']
                try:
                    movie['rate'] = get_movie_rate(movie['url'])
                except:
                    movie['rate'] = 0

                movie_list.append(movie)
            elif (check_score == 2):
                # 直接翻页
                continue
            else:
                # 跳出while循环
                till_end = True
                break

        i = i + 1
        print(u'---------第{}页处理完成。---------'.format(i))

    print(movie_list)
    return movie_list
    

def cal_average_rate(movie_list):
    '''
    计算平均得分。
    '''
    l = []
    for item in movie_list:
        if item['rate'] != 0:
            l.append(item['rate'])
    return float(sum(l)) / len(l)


if __name__ == '__main__':
    movie_list = get_user_watched_movies(123164315, '2016-01-01', '2016-12-31')
    # get_movie_rate('https://movie.douban.com/subject/26727273/')
    avg_rate = cal_average_rate(movie_list)
    print(avg_rate) # 7.52分！！
    

