#!/usr/bin/python3.9
from bs4 import BeautifulSoup

with open('followers_1.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')
    anchor_tags = soup.find_all("a")
    usernames = [tag.text for tag in anchor_tags]

    for username in usernames:
        print(username)
