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
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from base64 import *
import insta

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

def converse(post):
    pass


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

if __name__ == '__main__':
    main()
