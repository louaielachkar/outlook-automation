
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent


NAME = "Mike"

# start the chrome browser
def start_browser():
    options = Options()
    # options.headless = True
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--incognito")
    #ua = UserAgent()
    #userAgent = ua.random
    # options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver    

# login in outlook
def outlook_login(driver, email, password):
    print("***TRYING***:\n", email,password)
    url = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1623751479&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3dc20ad531-7dbc-9430-6bb4-fc415bb7e0f4&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015"
    driver.get(url)
    driver.maximize_window()
    while True:
        driver.find_element_by_name('loginfmt').send_keys(email, Keys.ENTER)
        sleep(2)
        break
    while True:
        try:
            sleep(2)
            driver.find_element_by_name('passwd').send_keys(password, Keys.ENTER)
            break
        except:
            pass
    print("Login complete")

# check and close outlook pop-ups
def check_popup(driver):
    try:
        driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]")
        driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]/span/span/span").click()
        print("popup closed")
    except NoSuchElementException:
        try:
            driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]/div[2]/div/div[1]/img")
            driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/span[3]/button/span/span/span").click()
            print("popup closed")
        except NoSuchElementException:
            pass

# search name to
def search_name(driver):
    while True:
        try:
            corner = driver.find_element_by_xpath("//*[@id='O365_MainLink_NavMenu']")
            action = ActionChains(driver)
            action.move_to_element_with_offset(corner, 500, 20)
            action.click()
            action.perform()
            driver.find_element_by_xpath("//*[@id='searchBoxId-Mail']/div[2]/div/input").send_keys(NAME, Keys.ENTER) 
            break
        except:
            pass