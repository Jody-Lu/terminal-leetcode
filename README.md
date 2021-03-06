============================
Terminal-Leetcode
============================
Terminal-Leetcode is a terminal based leetcode website viewer. It's not that obvious to use
terminal to view quizzes than use a web browser.  
This project is inspired by RTV.
![alt text](screenshots/list.png "quiz list" )
![alt text](screenshots/detail.png "quiz detail")
---------------

[![Build Status](https://travis-ci.org/chishui/terminal-leetcode.svg?branch=master)](https://travis-ci.org/chishui/terminal-leetcode)
[![PyPI](https://img.shields.io/pypi/v/nine.svg?maxAge=2592000)](https://pypi.python.org/pypi/terminal-leetcode)
[![PyPI](https://img.shields.io/badge/python-2.7-blue.svg?maxAge=2592000)](https://pypi.python.org/pypi/terminal-leetcode)

---------------
# Requirements
- Python 2.7  
- [Urwid](https://github.com/urwid/urwid)

# Installation
Install with pip  
```
 $ pip install terminal-leetcode
```
Clone the repository  
```
 $ git clone https://github.com/chishui/terminal-leetcode.git  
 $ cd terminal-leetcode  
 $ sudo python setup.py install  
```
# Usage
To run the program, input leetcode in terminal    
```
 $ leetcode
```
Quiz list will only be retrieved once from leetcode website, then the webpage will be stored locally.   
# Controls:
- Press ``H`` to see help infomation.  
- Press ``up`` and ``down`` to go through quiz list.  
- Press ``enter`` or ``right`` to see a quiz detail, and press ``left`` to go back.  
- Press ``R`` in quiz list view to retrieve quiz from website.  
Vim's moving keys ``h``, ``j``, ``k``, ``l`` are supported.

# TODO
- Test
- User login
- Quiz list sort
- ~~Install with pip~~
- Get quiz default code interface

# Contribute
All kinds of contributions are welcome.

# Licence
MIT

