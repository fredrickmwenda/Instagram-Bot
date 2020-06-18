from selenium import webdriver

from selenium.common.exceptions import InvalidElementStateException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

import time
import os
import configparser
import requests
import requests.utils
import urllib.request
import random
import emoji
import json

from story_util import watch_story

class InstagramBot:
    def __init__(self, username, password):

        self.username = username
        self.password = password

        self.base_url = 'https://www.instagram.com/'
        self.nav_user_url = 'https://www.instagram.com/{}/'
        self.get_tag_url = 'https://www.instagram.com/explore/tags/{}/'
        self.stories_link = 'https://www.instagram.com/stories/{}/'
        self.url_tag = 'https://www.instagram.com/explore/tags/'
       

        self.stories_watched = 0
        self.reels_watched = 0
       
        # download chromedriver setup and store it 
        # in the Instagram bot 
        self.driver = webdriver.Chrome('./chromedriver.exe')
        #for Mozilla firefox run
        # self.driver = webdriver.Firefox(
        #     executable_path="geckodriver",
        #     proxy=None,timeout=20,
        #     keep_alive=True
        # )
         
        self.session = requests.Session()
        # use this variable to terminate the nested loops after quotient
        # reaches
        self.quotient_breach = False
        self.aborting = False
        self.story_simulate = False
       
        self.login()
       

# ==============================================Login Section=====================================================================
    def login(self):
        self.driver.get('{}accounts/login'.format(self.base_url))
        
        time.sleep(5)
        #self.driver.find_element_by_<specify category to select from>();
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_xpath("//button[@type=\"submit\"]").click()              
        
        #set the time to sleep to avoid autologin
        time.sleep(10)


    def clear_notification(self):
        #turn_on_notification = self.find_element_by_xpath("//button[contains(text(), 'Turn On')]")
        turn_off_notification = self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
        turn_off_notification.click()
        # time.sleep(5)
        
    #Navigate to a user url
    def nav_user(self,user):
         self.driver.get(self.nav_user_url.format(user))

# ==========================================FOLLOW Section=========================================================================
    #Following Action
    def follow_user(self, user):
        self.nav_user(user)
        follow_button =  self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]")
        follow_button.click()
    
    #Unfollowing Action
    def unfollow_user(self, user):

        self.nav_user(user)
        unfollow_button =  self.driver.find_elements_by_xpath("//span[contains(@class,'glyphsSpriteFriend_Follow u-__7')]")
      
        #unfollow_button.click()
        if unfollow_button:
            for btn in unfollow_button:
                btn.click()
                time.sleep(5)
                unfollow_confirm = self.driver.find_elements_by_xpath("//button[contains(text(), 'Unfollow')]")[0]
                unfollow_confirm.click()
        else:
            print ('No button like that was found'.format('Following'))

    #Search action
    def search_sth(self, tag):
         self.driver.get(self.get_tag_url.format(tag))
    
# ========================================Like Action====================================================================
    def like_latest_post(self, user, posts, like=True):

        action = 'Like' if like else 'Unlike'
        self.nav_user(user)
        
        images = []
        images.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for image in images[:posts]:
            # image.click() 
            self.driver.execute_script("arguments[0].click();", image) 
            time.sleep(5) 
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                print(e)
            time.sleep(3)
            check = self.driver.find_elements_by_class_name('ckWGn')
            if len(check):
                # check[0].click()
                check[1].click()

        	

    def like_feed_post(self, amount):
        rand = random.randrange(2, amount)
        print("\item set selected m-->"+str(rand)+" Post Selected")
        time.sleep(3)
        for i in range(1, rand):
            likeElement = self.driver.find_element_by_xpath('//div/div[2]/div/article['+str(i)+']/div[2]/section[1]/span[1]/button')         
            time.sleep(30)            
            # likeElement.click()
            self.driver.execute_script("arguments[0].click();", likeElement)
            time.sleep(2)
            print("\The liked image m-->"+str(i)+" Post Liked")

    def Like_photoTags_and_comment(self, hashtag, comment, like=True):
        action = 'Like' if like else 'Unlike'

        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)       
        pic_hrefs = []
        for i in range(1, 3):
            self.driver.execute_script("window.scrollTo(0,document.scrollHeight);")
            time.sleep(2)
        #searching for pictures link
        hrefs_in_view = self.driver.find_elements_by_tag_name('a')
        # finding relevant hrefs
        hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                         if '.com/p/' in elem.get_attribute('href')]
        # building list of unique photos
        [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
        print("Check: pic href length " + str(len(pic_hrefs)))

        for pics in pic_hrefs:
            self.driver.get(pics)
            time.sleep(5)
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()    
            except NoSuchElementException:
                print('no such element has been found')

            if comment in self.driver.page_source:
                continue
            else:
                self.driver.find_element_by_class_name("Ypffh").click()
                for letter in comment:
                    self.driver.find_element_by_class_name("Ypffh").send_keys(letter)
                    time.sleep(random.randint(1,2))
                self.driver.find_element_by_class_name("Ypffh").send_keys(Keys.ENTER)
                time.sleep(5)

    # Like  Photos in a tag by specifying  their amount
    def Likes_photoTags(self, tag, posts, like=True):
        action = 'Like' if like else 'Unlike'

        self.driver.get("https://www.instagram.com/explore/tags/" + tag + "/")
        time.sleep(2)       
        pic_hrefs = []
        for i in range(1, 5):
            self.driver.execute_script("window.scrollTo(0,document.scrollHeight);")
            time.sleep(2)
        #searching for pictures link
        hrefs_in_view = self.driver.find_elements_by_tag_name('a')
        # finding relevant hrefs
        hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                         if '.com/p/' in elem.get_attribute('href')]
        # building list of unique photos
        [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
        print("Check: pic href length " + str(len(pic_hrefs)))

        for pics in pic_hrefs[:posts]:
            self.driver.get(pics)
            time.sleep(10)
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()    
            except NoSuchElementException:
                print('no such element has been found')
                time.sleep(5)

# ======================================Comment Section=================================================================
    
     #Comments on a post that is in modal form/ user liked post from navigated profile
    def comment_post(self, text):
        
        comment_input = self.driver.find_element_by_class_name('Ypffh')
        comment_input.click()
        comment_input.send_keys(text)
        comment_input.send_keys(Keys.Return)
        print('Comment Zone')


    # Commenting on feed post some test pending
    def get_comment_input(self):
        comment_input = self.driver.find_elements_by_xpath('//form/textarea')
        if len(comment_input) <= 0:
            comment_input = self.driver.find_elements_by_class_name('Ypffh')

        return comment_input

    def open_comment_section(self):
        comment_elem = self.driver.find_element_by_xpath("//button[*[local-name()='svg']/@aria-label='Comment']")
         
    def comment_image(self, comments): # user,
        #username set to user
        """Checks if it should comment on the image"""
        # self.nav_user(user)

        rand_comment = random.choice(comments)
        rand_comment = emoji.demojize(rand_comment)
        rand_comment = emoji.emojize(rand_comment, use_aliases=True)

        comment_section = self.driver.find_element_by_xpath("//button[*[local-name()='svg']/@aria-label='Comment']")
        # comment_section.click()
        self.driver.execute_script("arguments[0].click();", comment_section)
        # open_comment_section()
        time.sleep(3)
   
        comment_input = self.get_comment_input()
        try:
            if len(comment_input) > 0:
            # wait, to avoid crash
                time.sleep(2)
                comment_input = self.get_comment_input()
                # below, an extra space is added to force
                # the input box to update the reactJS core
                comment_input2 = self.get_comment_input()
                comment_to_be_sent = rand_comment

                # wait, to avoid crash
                time.sleep(5)
                #Insert the random Comment and post it.
                try:
                    ActionChains(self.driver).move_to_element(comment_input[0]).click().send_keys(comment_to_be_sent).send_keys(Keys.RETURN).perform()
                except StaleElementReferenceException:
                    print("The Dom Elements have changed")

                # wait, to avoid crash
                time.sleep(5)
   
                print("--> Comment Action successfull")
                return True, "success"

            else:
                print("--> Comment Action Likely Failed!" "\t~comment Element was not found")
                return False, "commenting disabled"

        except InvalidElementStateException:
            print("--> Comment Action Likely Failed!","\t~encountered `InvalidElementStateException` :/")
            return False, "invalid element state"
            
        print("--> Commented: {}".format(rand_comment.encode("utf-8")))
        return True, "success"


    
# ====================================STORIES=========================================================================
 
    def stories_all(self):
        # gather all the stories
        stories = []
        stories = self.driver.find_elements_by_class_name('Ckrof')
        # Iterate for the list of stories
        for i in range(3, len(stories)+3):
        # Expand each node
            node_expand_icon = self.driver.find_element_by_xpath("//div/div/div/div/ul/li[" + str(i) + "]")
            if node_expand_icon:
                # for link in node_expand_icon:
                #     link.click()
                button = self.driver.find_element_by_xpath("//div/div[1]/div/div/button/div")
                self.driver.execute_script("arguments[0].click();", button)
            self.driver.execute_script("arguments[0].click();", node_expand_icon)

       
    def story_by_tags(self, tags: list = None):
        """ Watch stories for specific tag(s) """
        if self.aborting:
            return self

        if tags is None:
            print("No Tags set")
        else:
            # iterate over set tags
            for index, tag in enumerate(tags):
                if self.quotient_breach:
                    break

                
                time.sleep(3)
                if len(tags) > 1:
                    print("Tag [{}/{}]".format(index + 1, len(tags)))
                print("Loading stories with Tag --> {}".format(tag.encode("utf-8")))
                
                time.sleep(2)
                try:
                    reels = watch_story(self.driver, tag, "tag", self.story_simulate)
                except NoSuchElementException:
                    print("No stories skipping this tag")
                    continue
                if reels > 0:
                    self.stories_watched += 1
                    self.reels_watched += reels

    def story_by_users(self, users: list = None):
        """ Watch stories for specific user(s)"""
        if self.aborting:
            return self

        if users is None:
            print("No users passed to story_by_users")
        else:
            # iterate over set users
            for index, user in enumerate(users):
                if self.quotient_breach:
                    break

                if len(users) > 1:
                    print("User [{}/{}]".format(index + 1, len(users)))
                print("Loading stories with User --> {}".format(user.encode("utf-8")))

                try:
                    reels = watch_story(self.driver, user, "user", self.story_simulate)
                except NoSuchElementException:
                    print("No stories skipping this user")
                    continue
                if reels > 0:
                    self.stories_watched += 1
                    self.reels_watched += reels

       

#  ==========================================================================================================================

if __name__ == '__main__':
    #create a config file to pass ur
    #instagram name and password
    confparser = configparser.ConfigParser()
    confparser.read(os.path.expanduser('./check.ini'))

    username = confparser['AUTH']['USERNAME']
    password = confparser['AUTH']['PASSWORD']

    bot = InstagramBot(username,password)
    bot.clear_notification()
    bot.like_feed_post(10)
    bot.comment_image(['Awesome', 'Nice Shot!'])
    bot.nav_user('teamdreamvillefacts')
    bot.search_sth('jcole')
    bot.follow_user('ronaldo')
    bot.story_by_users(['teamdreamvillefacts', 'martialfc'])
    bot.story_by_tags(['soccer'])
    bot.unfollow_user('ronaldo')
    bot.Like_photoTags_and_comment('neymar','Wow')
    bot.like_latest_post('martialfc', 10, like=True)
    bot.comment_post('awesome')
    bot.stories_all()

 

    