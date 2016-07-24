import os
import requests
from bs4 import BeautifulSoup
from .model import QuizItem

BASE_URL = 'https://leetcode.com'
HOME_URL = BASE_URL + '/problemset/algorithms'
HOME = os.path.expanduser('~')
CONFIG = os.path.join(HOME, '.config', 'leetcode')
DATA_FILE = os.path.join(CONFIG, 'leetcode_home.txt')

class Leetcode(object):
    def __init__(self):
        self.items = []

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
        title = ""
        body = ""
        text = retrieve(BASE_URL + item.url).encode('utf-8')
        bs = BeautifulSoup(text, 'html.parser')
        tmp_title = bs.find('div', 'question-title')
        if tmp_title: title = tmp_title.h3.text
        #title = bs.find('div', 'question-title').h3.text
        tmp_body = bs.find('div', 'question-content')
        if tmp_body: body = tmp_body.text.replace(chr(13), '')
        return title, body

    def retrieve_all_problems(self):
        """
        :rtype: title_list, body_list
        """
        if not self.items: return None
        title_list = []
        body_list = []

        for item in self.items:
            title, body = self.retrieve_detail(item)
            if title: title_list.append(title)
            if body: body_list.append(body)

        return title_list, body_list


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
