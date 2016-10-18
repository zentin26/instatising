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

def instagram_login(driver, username, password):
    driver.get('https://www.instagram.com/accounts/login/?force_classic_login')
    driver.find_element_by_id('id_username').send_keys(username)
    driver.find_element_by_id('id_password').send_keys(password)
    driver.find_element_by_class_name('button-green').click()

    return True

def parse_numstring(s):
    s = s.split(' ')[0]
    s = s.replace(',', '')
    s = s.replace('.', '')

    s = s.replace('k', '000') # thousands
    s = s.replace('m', '000000') # millions
    s = s.replace('b', '000000000') # billions

    return int(s)

def instagram_search(query):
    driver.get('http://www.instagram.com/')



def get_hashtag_posts(hashtag):
    pass

class InstagramPost():
    def __init__(self, post_id, post_user=None, num_likes=None, post_type=None, caption=None, location=None):
        self.post_user = post_user
        self.num_likes = num_likes
        self.post_type = post_type
        self.postid = post_id
        self.caption = caption
        self.location = location

        self.postimage = None
        self.post_subject = None
        

    def get_comments(self, max_comments=float('inf')):
        driver.get('http://www.instagram.com/p/' + self.postid)

        # box = driver.find_element_by_class_name('ul._mo9iw._123ym')
        # comment = driver.find_element_by_class_name('ul._mo9iw._123ym').find_elements_by_tag_name('li')
        top = None

        while (driver.find_element_by_class_name('ul._mo9iw._123ym').find_elements_by_tag_name('li')[-1] != top) and (len(driver.find_element_by_class_name('ul._mo9iw._123ym').find_elements_by_tag_name('li')) < max_comments):
            top = driver.find_element_by_class_name('ul._mo9iw._123ym').find_elements_by_tag_name('li')[-1]

            driver.execute_script('arguments[0].scrollTo(100, arguments[0].scrollHeight);', driver.find_element_by_class_name('ul._mo9iw._123ym'))
            time.sleep(2)
 
        v = driver.find_element_by_class_name('ul._mo9iw._123ym').find_elements_by_tag_name('li')
        for c in v:
            comment_user = c.find_element_by_tag_name('a').text
            comment_body = c.find_element_by_tag_name('span').text

            c = InstagramComment(comment_user, comment_body, self)
            self.comments.append(c)

        return self.comments

    def like(self, driver):
        driver.get('http://www.instagram.com/p/' + self.postid)

        driver.find_element_by_css_selector('span._soakw.coreSpriteHeartOpen').click()

        return True

    def unlike(self, driver):
        driver.get('http://www.instagram.com/p/' + self.postid)

        driver.find_element_by_css_selector('span._soakw.coreSpriteHeartFull').click()

        return True

    def get_subject(self, driver):
        driver.get('http://www.instagram.com/p/' + self.postid)
        image = driver.find_element_by_class_name('img._icyx7').find_element_by_tag_name('li').get_attribute('href')

        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img = Image.open(file)
        pass

    def get_caption(self, driver):
        driver.get('http://www.instagram.com/p/' + self.postid)

        c = driver.find_element_by_class_name('ul._mo9iw._123ym').find_element_by_tag_name('li')
        comment_user = c.find_element_by_tag_name('a').text
        comment_body = c.find_element_by_tag_name('span').text
        hashtags, attags = parse_comment(c)
        c = InstagramComment(comment_user, comment_body, self, hashtags, attags)
        self.caption = c

        return self.caption

    def get_location(self, driver):
        driver.get('http://www.instagram.com/p/' + self.postid)

        self.location = driver.find_element_by_css_selector('a_kul9p._rnlnu').text

        return self.location

class InstagramUser():
    def __init__(self, username, posts=[], following=[], followers=[], bio=None):
        self.username = username
        self.posts = posts
        self.following = following
        self.followers = followers
        self.bio = bio

        self.user_subject = None

    def get_followers(self, driver, recursive=False, max_followers=800):
        driver.get('https://www.instagram.com/' + self.username)

        try:
            numf = parse_numstring(driver.find_element_by_xpath('//a[@href="/' + self.username + '/followers/"]').text)
            driver.find_element_by_xpath('//a[@href="/' + self.username + '/followers/"]').click()

        except:

            return False

        # box = driver.find_element_by_class_name('_4gt3b')
        # users = driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')
        users = []
        botm = None

        while (driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')[-1] != botm) and (len(driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')) < max_following):
            botm = driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')[-1]

            driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);', driver.find_element_by_class_name('_4gt3b'))
            time.sleep(2) # fuck you Selenium developers for not implimenting a boolean condition wait.
 
        v = driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')
        for u in v:
            u =  InstagramUser(u.find_elements_by_tag_name('a')[-1].text)
            users.append(u)

        users1 = []

        if recursive:
            def _merge(u):
                if (not u in users) and u:
                    users1.append(u)

            for user in users:
                us = user.get_followers(driver, recursive-1)

                if us:
                    map(_merge, us)

        users1 += users
        self.followers = users1

        return self.followers

    def get_following(self, driver, recursive=False, max_following=800):
        driver.get('https://www.instagram.com/' + self.username)

        try:
            numf = parse_numstring(driver.find_element_by_xpath('//a[@href="/' + self.username + '/following/"]').text)
            driver.find_element_by_xpath('//a[@href="/' + self.username + '/following/"]').click()

        except:
            traceback.print_exc()

            return False

        # box = driver.find_element_by_class_name('_4gt3b')
        # users = driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')
        users = []
        botm = None

        while (driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')[-1] != botm) and (len(driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')) < max_following):
            botm = driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')[-1]
 
            driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);', driver.find_element_by_class_name('_4gt3b'))
            time.sleep(3)

        v = driver.find_element_by_class_name('_4gt3b').find_elements_by_tag_name('li')
        for u in v:
            u =  InstagramUser(u.find_elements_by_tag_name('a')[-1].text)
            users.append(u)

        users1 = []

        if recursive:
            def _merge(u):
                if (not u in users) and u:
                    users1.append(u)

            for user in users:
                us = user.get_following(driver, recursive-1)

                if us:
                    map(_merge, us)

        users1 += users
        self.following = users1

       return self.following

    def follow(self, driver):
        try:
            driver.get('https://www.instagram.com/' + self.username)
            driver.find_element_by_css_selector('button._aj7mu._2hpcs._kenyh._o0442').click()

            return True    

        except selenium.common.exceptions.NoSuchElementException: # if user is already followed

            return False

    def unfollow(self, driver):
        try:
            driver.get('https://www.instagram.com/' + usr)
            driver.find_element_by_css_selector('button._aj7mu._r4e4p._kenyh._o0442').click()

            return True   

        except selenium.common.exceptions.NoSuchElementException:
           driver.find_element_by_css_selector('button._aj7mu._96gf6._kenyh._o0442').click() # if private account request

           return True

    def get_subject(self, driver):
        pass

    def get_bio(self, driver):
        driver.get('https://www.instagram.com/' + self.username)

        self.bio = driver.find_element_by_css_selector('div._bugdy').text

        return self.bio

    def get_posts(self, driver, num_posts=3):
        driver.get('https://www.instagram.com/' + self.username)

        if parse_numstring(driver.find_element_by_css_selector('span._s53mj').text) < numposts: # number of posts

            return False

        elif len(driver.find_elements_by_css_selector('a._8mlbc._vbtk2._t5r8b')) < numposts:
            driver.find_element_by_css_selector('._oidfu').click()
            while len(driver.find_elements_by_css_selector('a._8mlbc._vbtk2._t5r8b')) < numposts:
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

        self.posts = []
        for p in driver.find_elements_by_css_selector('a._8mlbc._vbtk2._t5r8b'):
            p = InstagramPost(p.get_attribute('href').split('/')[-2])
            self.posts.append(p)
                
            if len(self.posts) >= numposts:
                break
    
        return self.posts


class InstagramComment():
    def __init__(self, user, text, post=None, hashtags=[], attags=[])
        self.user = user
        self.text = text
        self.post = post
        self.hashtags = hashtags
        self.attags = attags

    def get_hashtags(self, driver):
        hashtags = re.findall(r'#(\w+)', c)

        return hashtags

    def get_attags(self, driver):
        attags = re.findall(r'@(\w+)', c)

        return attags


def firefox_tor():
    profile=webdriver.FirefoxProfile()
    profile.set_preference('places.history.enabled', False)
    profile.set_preference('privacy.clearOnShutdown.offlineApps', True)
    profile.set_preference('privacy.clearOnShutdown.passwords', True)
    profile.set_preference('privacy.clearOnShutdown.siteSettings', True)
    profile.set_preference('privacy.sanitize.sanitizeOnShutdown', True)
    profile.set_preference('signon.rememberSignons', False)
    profile.set_preference('network.cookie.lifetimePolicy', 2)
    profile.set_preference('network.dns.disablePrefetch', True)
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9050)
    profile.set_preference('network.proxy.socks_remote_dns', True)

    return profile

def main():
    display = Display(visible=1)
    display.start()

    driver = webdriver.Firefox()

    username = "huntanium_"
    password = b64decode('b2tpanVoMTIz')

    try:
        login(driver, username, password)

    except:
        traceback.print_exc()

    finally:
        #driver.quit()
        #display.stop()

if __name__ == '__main__':
    main()
