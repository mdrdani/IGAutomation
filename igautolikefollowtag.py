from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import random

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        #Jika Menggunakan Linux hapus *.exe 
        #Jika Menggunakan Windows tambahkan *.exe
        self.driver = webdriver.Chrome('./assets/chromedriver.exe')
    
    def closeBrowser(self):
        self.driver.close()
    
    def login(self):
        #membuka chrome dan ke situs tujjuan
        driver = self.driver
        driver.get('https://www.instagram.com/')
        time.sleep(2)

        #cari tombol login
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)

        #masukan username
        username_element = driver.find_element_by_xpath("//input[@name='username']")
        username_element.clear()
        username_element.send_keys(self.username)

        #masukan password
        password_element = driver.find_element_by_xpath("//input[@name='password']")
        password_element.clear()
        password_element.send_keys(self.password)
        password_element.send_keys(Keys.RETURN)
        time.sleep(2)

    def likefoto(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)
        for i in range(1,3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        #mencari untuk mencari link foto dan di simpan di array
        pic_hrefs = []
        for i in range(1,2):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("Check: Banyak Foto " + str(len(pic_hrefs)))
            except Exception:
                continue

        #Like Foto yang sudah di kumpulkan 
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2, 4))
                #action Follow Account
                follow_button = driver.find_element_by_css_selector('button')
                if(follow_button.text != 'Following'):
                    follow_button.click()
                    time.sleep(2)
                else:
                    print("Kamu Sudah Follow User ini")
                
                #action comment
                time.sleep(random.randint(2, 4))
                comment_box = lambda: driver.find_element_by_xpath('//textarea[@aria-label="Add a comment…"]').click()
                comment_box().click()
                comment_box.send_keys('Test')
                comment_box.send_keys(Keys.ENTER)
                time.sleep(1)
                
                #mencari element tombol love dan perintah klik 
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    print("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(1)
            except Exception as e:
                time.sleep(2)
            unique_photos -= 1


bot = InstagramBot("timsuksesig","Mayday123good")
bot.login()
hashtags = ['cebong']
[bot.likefoto(tag)  for tag in hashtags]
bot.closeBrowser()

