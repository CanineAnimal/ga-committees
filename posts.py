#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 ... 2021
@author: ifly6
"""
# Substantially modified by Merni

import re
import time
from collections import namedtuple

import requests
from bs4 import BeautifulSoup
import sqlite3

Post = namedtuple('Post', ['number', 'title', 'post'])
# number : resolution number (added by Merni)
# title : name of resolution
# post : forum post ID (viewtopic.php?t=30#p=NNN)

url = 'https://forum.nationstates.net/viewtopic.php?f=9&t=30&start={}'

# create containers and helper functions for parsing
seen_list = []
titles_and_posts = []



def is_empty(i):
    post_text = post_title.parent.parent.select('div.content')[0].text.strip()

    # normal posts should never start with a full stop
    if (post_text.startswith('.') or len(post_text) == 0):
        return True

    return False

resno = 1 # Resolution number (GA NNN)

# parse the raw forum data
no_more = False
for i in range(0, 40):
    if no_more:
        break

    adj_value = i * 25
    adj_url = url.format(adj_value)
    print(f'getting posts {i}')

    soup = BeautifulSoup(requests.get(adj_url).text, 'lxml')
    for post_title in soup.select('div.postbody h3 a'):
        if post_title['href'] in ['#p309', '#p310']:
            # don't attempt to parse the intro and table!
            continue

        if post_title['href'] in seen_list:
            no_more = True
            break

        try:
            text = post_title.parent.parent.select('div.content span')[0].text
        except IndexError:
            text = ''
        
        if is_empty(post_title): continue

        text = re.sub(r'\[.*\]', '', text)

        titles_and_posts.append(Post(
            resno,
            text,
            re.search(r'\d+', post_title['href'])[0]))
        seen_list.append(post_title['href'])
        
        resno += 1
    
    time.sleep(5)

print("Adding to database")

# Add the list to the database - Merni

con = sqlite3.connect('wacdb')
cur = con.cursor()
cur.execute('DELETE FROM resolutions')
for res in titles_and_posts:
    url = "https://forum.nationstates.net/viewtopic.php?p={}#p{}".format(res.post, res.post)
    cur.execute("INSERT INTO resolutions (res, resname, url) VALUES (?, ?, ?)", (res.number, res.title, url))

con.commit()
con.close()
