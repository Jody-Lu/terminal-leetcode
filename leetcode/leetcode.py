import os
import requests
from bs4 import BeautifulSoup
from .model import QuizItem
from threading import Thread

BASE_URL = 'https://leetcode.com'
HOME_URL = BASE_URL + '/problemset/algorithms'
HOME = os.path.expanduser('~')
CONFIG = os.path.join(HOME, '.config', 'leetcode')
DATA_FILE = os.path.join(CONFIG, 'leetcode_home.txt')
title_body = {}

class GetUrlThread(Thread):
    def __init__(self, url):
        self.url = url
        super(GetUrlThread, self).__init__()

    def run(self):
        text = retrieve(self.url).encode('utf-8')
        bs = BeautifulSoup(text, 'html.parser')
        title = bs.find('div', 'question-title').h3.text
        body = bs.find('div', 'question-content').text.replace(chr(13), '')
        title_body[title] = body

class Leetcode(object):
    def __init__(self):
        self.items = []
        self.title_body = {}

    def __getitem__(self, i):
        return self.items[i]

    def hard_retrieve_home(self):
        text = retrieve(HOME_URL).encode('utf-8')
        save_data_to_file(text, DATA_FILE)
        return self.parse_home(text)

    # retrieve all problems as QuizItems
    def retrieve_home(self):
        if not os.path.exists(DATA_FILE):
            return self.hard_retrieve_home()
        text = load_data_from_file(DATA_FILE)
        return self.parse_home(text)

    # parse the retrieving html file (text)
    def parse_home(self, text):
        bs = BeautifulSoup(text, 'html.parser')
        trs = bs.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) < 3:
                continue
            item = QuizItem(tds[1].text, tds[2].a.text, tds[2].a['href'], tds[3].text,
                            tds[-1].text, tds[2].find('i', 'fa-lock') != None)
            self.items.append(item)

        return self.items

    def retrieve_detail(self, item):
        """
        :item: QuizItem
        If the problem is locked, it will fail to get the title & body
        """
        if item.lock: return "", ""

        key_title = item.id + ". " +  item.title
        if key_title in self.title_body:
            return item.title, self.title_body[key_title]

        text = retrieve(BASE_URL + item.url).encode('utf-8')
        bs = BeautifulSoup(text, 'html.parser')
        title = bs.find('div', 'question-title').h3.text
        body = bs.find('div', 'question-content').text.replace(chr(13), '')
        self.title_body[title] = body
        return title, body


    def retrieve_all_problems(self):
        """
        :rtype: title_list, body_list
        """
        if not self.items: return None

        threads = []
        for item in self.items[:100]:
            if item.lock: continue
            t = GetUrlThread(BASE_URL + item.url)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        self.title_body = title_body

# Retrieve URL
def retrieve(url):
    r = requests.get(url)
    # check http response
    if r.status_code != 200:
        return None

    return r.text

def save_data_to_file(data, filename):
    filepath = os.path.dirname(filename)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(filename, 'w') as f:
        f.write(data)

def load_data_from_file(path):
    with open(path, 'r') as f:
        return f.read()
