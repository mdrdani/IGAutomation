from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import random
from random import randint

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('./assets/chromedriver.exe')
    
    def closeBrowser(self):
        self.driver.close()
    
    def login(self):
        #membuka chrome dan ke situs tujuan
        driver = self.driver
        driver.get('https://www.instagram.com/')
        time.sleep(2)

        #cari tombol login
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)

        #mencari element dan masukan username
        username_element = driver.find_element_by_xpath("//input[@name='username']")
        username_element.clear()
        username_element.send_keys(self.username)

        #mencari element dan masukan password
        password_element = driver.find_element_by_xpath("//input[@name='password']")
        password_element.clear()
        password_element.send_keys(self.password)
        password_element.send_keys(Keys.RETURN)
        time.sleep(2)

    def likefollowfoto(self, profile):
        driver = self.driver
        #url
        driver.get("https://www.instagram.com/" + profile + "/")
        time.sleep(2)
        #action Follow Account
        follow_button = driver.find_element_by_css_selector('button')
        if(follow_button.text != 'Following'):
            follow_button.click()
            time.sleep(2)
        else:
            print("Kamu Sudah Follow User ini")

        #action scroll ke bawah untuk mencari foto foto
        for i in range(1,3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        #mencari untuk mencari link foto
        pic_hrefs = []
        for i in range(1,2):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags from profile account
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("Check: Banyak Foto " + str(len(pic_hrefs)))
            except Exception:
                continue

        #Jika sudah di temukan link foto lakukan perintah Like pada banyak foto yang
        # ditemukan
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:        
                #action comment
                time.sleep(random.randint(2, 4))
                comment_box = lambda: driver.find_element_by_xpath('//textarea[@aria-label="Add a comment…"]').click()
                comment_box().click()
                comment_box.send_keys('Test')
                comment_box.send_keys(Keys.ENTER)
                time.sleep(1)

                #like button
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    print("#" + profile + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(1)

            except Exception as e:
                time.sleep(2)
            unique_photos -= 1


#input username and password ("username","password")
bot = InstagramBot("timsuksesig","Mayday123good")
bot.login()

#input account username
follprof = ['cehamot']
[bot.likefollowfoto(folprof)  for folprof in follprof]

#close browser automatic
bot.closeBrowser()

