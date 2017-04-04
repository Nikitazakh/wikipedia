#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt
import codecs
import statistics

class WikiGraph():
    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with codecs.open(filename, 'r', 'utf_8_sig') as f:
            l = f.readline()
            (n, _nlinks) = (int(list(map(str, l.split()))[0]), int(list(map(str, l.split()))[1])) # TODO: прочитать из файла

            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))

            for i in range(n):
                self._titles.append(f.readline().rstrip())
                l = f.readline()
                l_1 = list(map(int, l.split()))
                self._sizes[i] = l_1[0]
                self._redirect[i] = l_1[1]
                self._offset[i+1] = self._offset[i]+l_1[2]
                for j in range(self._offset[i], self._offset[i+1]):
                    self._links[j] = int(f.readline())

            # TODO: прочитать граф из файла

        print('Граф загружен')




    def get_number_of_links_from(self, _id):
        return self._offset[id+1]

    def get_links_from(self, _id):
        links = []
        for i in range(self._offset[_id], self._offset[_id+1]):
            links.append(self._links[i])
        return links


    def get_id(self, title):
        return self._titles.index(title)

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        pass

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]

    def way(self, start, finish, used = None):
        start = self._titles.index(start)
        finish = self._titles.index(finish)
        print('Запускаем поиск в ширину')
        color = [10**9]*len(self._titles)
        color[start] = 0
        if used == None:
            used = set()
        used.add(start)
        Q = [start]
        while Q:
            if color[finish] != 10**9:
                break
            current = Q.pop(0)
            for neighbour in self._links[self._offset[current]:self._offset[current+1]]:
                if neighbour not in used and color[neighbour] > color[current]+1:
                    used.add(neighbour)
                    Q.append(neighbour)
                    color[neighbour] = color[current] + 1
        way = [self._titles[finish]]
        current = finish
        while current != start:
            for neighbour in self._links[self._offset[current]:self._offset[current + 1]]:
                if color[neighbour] == color[current] - 1:
                    way.append(self._titles[neighbour])
                    current = neighbour
        print('Поиск закончен. Найден путь:')
        return way[::-1]
    def number_of_redirect(self):
        num = 0
        for i in range(len(self._titles)):
            if self._redirect[i] != 0:
                num += 1
        return num

    def minimal_number_of_links(self):
        m = self._offset[1]
        for i in range(len(self._titles)):
            if self._offset[i+1] - self._offset[i] < m:
                m = self._offset[i+1] - self._offset[i]
        return m

    def max_number_of_article(self):
        m = 0
        for i in range(len(self._titles)):
            if self._offset[i + 1] - self._offset[i] > m:
                m = self._offset[i + 1] - self._offset[i]
        return m

    def number_of_article_with_min_num_of_links(self):
        m = self._offset[1]
        num = 0
        for i in range(len(self._titles)):
            if self._offset[i + 1] - self._offset[i] < m:
                m = self._offset[i + 1] - self._offset[i]
        for i in range(len(self._titles)):
            if self._offset[i+1] - self._offset[i] == m:
                num += 1
        return num

    def number_of_article_with_max_num_of_links(self):
        m = 0
        num = 0
        for i in range(len(self._titles)):
            if self._offset[i + 1] - self._offset[i] > m:
                m = self._offset[i + 1] - self._offset[i]
        for i in range(len(self._titles)):
            if self._offset[i+1] - self._offset[i] == m:
                num += 1
        return num

    def article_with_max_number_of_links(self):
        m = self._offset[1]
        ind = 0
        for i in range(len(self._titles)):
            if self._offset[i + 1] - self._offset[i] > m:
                m = self._offset[i + 1] - self._offset[i]
                ind = i
        return self._titles[ind]

    def middle_number_of_links(self):
        links = []
        for i in range(len(self._titles)):
            links.append(self._offset[i+1]-self._offset[i])
        return statistics.mean(links)

    def min_number_of_links_on_article(self):
        m = len(self._titles)
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if i in self._links[self._offset[j]:self._offset[j+1]]:
                    w += 1
            if w < m:
                m = w
        return m

    def num_of_articles_with_min_number_of_links_on(self):
        m = len(self._titles)
        num = 1
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if i in self._links[self._offset[j]:self._offset[j + 1]]:
                    w += 1
            if w < m:
                m = w
                num = 1
            elif w == m:
                num += 1
        return num

    def max_number_of_links_on_article(self):
        m = 0
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if i in self._links[self._offset[j]:self._offset[j + 1]]:
                    w += 1
            if w > m:
                m = w
        return m

    def num_of_articles_with_max_number_of_links_on(self):
        m = 0
        num = 1
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if i in self._links[self._offset[j]:self._offset[j + 1]]:
                    w += 1
            if w > m:
                m = w
                num = 1
            elif w == m:
                num += 1
        return num

    def article_with_max_number_of_links_on(self):
        m = 0
        ind = 0
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if i in self._links[self._offset[j]:self._offset[j + 1]]:
                    w += 1
            if w > m:
                ind = i
                m = w
        return self._titles[ind]

    def middle_num_of_links_on_article(self):
        sum = 0
        num = 0
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if i in self._links[self._offset[j]:self._offset[j + 1]]:
                    w += 1
            sum += w
            num += 1
        return sum/num

    def min_num_of_redir_on_article(self):
        m = len(self._titles)
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if self._redirect[j] == i+1:
                    w += 1
            if w < m:
                m = w
        return m

    def num_of_article_with_min_num_of_redir_on(self):
        m = len(self._titles)
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if self._redirect[j] == i+1:
                    w += 1
            if w < m:
                m = w
        return self._redirect.count(m)

    def max_num_of_redir_on_article(self):
        m = 0
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if self._redirect[j] == i+1:
                    w += 1
            if w > m:
                m = w
        return m

    def num_of_article_with_max_num_of_redir_on(self):
        m = 0
        num = 1
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if self._redirect[j] == i+1:
                    w += 1
            if w > m:
                num = 1
                m = w
            elif w == m:
                num += 1
        return num

    def article_with_max_num_of_redir_on(self):
        m = 0
        ind=0
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)): #ddd
                if self._redirect[j] == i+1:
                    w += 1
            if w > m:
                ind = i
                m = w
        return self._titles[ind]

    def middle_num_of_redir_on_article(self):
        red = [0]*len(self._titles)
        for i in range(len(self._titles)):
            w = 0
            for j in range(len(self._titles)):
                if self._redirect[j] == i+1:
                    w += 1
            red[i] = w
        return statistics.mean(red), statistics.stdev(red)
def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':
    a = WikiGraph()
    a.load_from_file('wiki_small.txt')
    print(*a.way('Python', 'Список_файловых_систем'))
    print('Количество статей с перенаправлением:', a.number_of_redirect())
    print('Минимальное количество ссылок из статьи:', a.minimal_number_of_links())
    print('Количество статей с минимальным количеством ссылок:', a.number_of_article_with_min_num_of_links())
    print('Максимальное количество ссылок из статьи:', a.max_number_of_article())
    print('Количество статей с максимальным количеством ссылок:', a.number_of_article_with_max_num_of_links())
    print('Статья с наибольшим количеством ссылок:', a.article_with_max_number_of_links())
    print('Среднее количество ссылок в статье:', a.middle_number_of_links())
    print('Минимальное количество ссылок на статью:', a.min_number_of_links_on_article())
    print('Количество статей с минимальным количеством внешних ссылок:', a.num_of_articles_with_min_number_of_links_on())
    print('Максимальное количество ссылок на статью:', a.max_number_of_links_on_article())
    print('Количество статей с максимальным количеством внешних ссылок:', a.num_of_articles_with_max_number_of_links_on())
    print('Статья с наибольшим количеством внешних ссылок:', a.article_with_max_number_of_links_on())
    print('Среднее количество внешних ссылок на статью:', a.middle_num_of_links_on_article())
    print('Минимальное количество перенаправлений на статью:', a.min_num_of_redir_on_article())
    print('Количество статей с минимальным количеством внешних перенаправлений:', a.num_of_article_with_min_num_of_redir_on())
    print('Максимальное количество перенаправлений на статью:', a.max_num_of_redir_on_article())
    print('Количество статей с максимальным количеством внешних перенаправлений:', a.num_of_article_with_max_num_of_redir_on())
    print('Статья с наибольшим количеством внешних перенаправлений:', a.article_with_max_num_of_redir_on())
    a,b = a.middle_num_of_redir_on_article()
    print('Среднее количество внешних перенаправлений на статью:', a, '(ср. откл.',b,')')
    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    # TODO: статистика и гистограммы