#!/usr/bin/python
import traceback
import sys
import re
import json
import time
import urllib
import cStringIO
import random
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from base64 import *
from stat_parser import Parser
import insta
driver = None
text_parser = Parser()
username = ''
password = ''

#####################################################
#
# 1.) get realted words to our keyword
# 2.) get relevant users and hashtags
# 3.) get relevant posts
# 4.) engage in basic conversation with other users
#   1.) parse user comment question
#   2.) decide response
#   3.) parse response into english
#   4.) write comment
#
#####################################################

def get_related_keywords(word):
    pass

def search(keywords):
    pass

def get_posts(users=[], hashtags=[]):
    pass

def get_meaning(text):
    text = text_parser(text)

    
    return 

def converse(post):
    # parse comment
    comments = post.get_comments(driver, max_comments=10)
    comments = filter(lambda x: x.get_attags(username), comments)

    for comment in comments:
        sentences = get_meaning(comment.text)
        
        
def main():
    display = Display(visible=1)
    display.start()
    
    driver = webdriver.Firefox()

    username = '' #sys.argv[1]
    password = '' #sys.argv[2]

    try:
        insta.instagram_login(driver, username, password)
        users = insta.user_search(driver, 'david')
        for u in users:
            print u, u.username

    except:
        traceback.print_exc()

    finally:
        driver.quit()
        display.stop()

questions = [('', ''), # (question, answer)
             ('', ''),
             ('', '')]
        
        
if __name__ == '__main__':
    main()
