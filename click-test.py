from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import threading
import random
import helper

NUM_OF_CLICKS = 20

def click_link(driver):
    for i in range(NUM_OF_CLICKS):
        while True:
            try:
                driver.find_element_by_xpath("//*[contains(text(),'It is yours now')]").click()
                if (i % 3 == 0):
                    try:
                        driver.find_element_by_xpath("//span[text()='Archiver']").click()
                        print("Archived")
                    except NoSuchElementException:
                        try:
                            elements = driver.find_elements_by_xpath("//span[text()='Archive']")
                            elements[1].click()
                        except:
                            pass
                for j in range (i):
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.DOWN)
                    actions.perform()
                    sleep(0.2)
                break
            except:
                pass
            
        while True:
            try:
                try:
                    driver.find_element_by_xpath("//*[@id='ReadingPaneContainerId']/div/div/div/div[2]/div[1]/div/div[3]/div/div/div/p[2]/a").click()
                except NoSuchElementException:
                    driver.find_element_by_xpath("//*[@id='ReadingPaneContainerId']/div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div/div/div/p[2]/a").click()
                sleep(7)
                parent = driver.window_handles[0]
                chld = driver.window_handles[1]
                driver.switch_to.window(chld)
                driver.close()
                driver.switch_to.window(parent)
                break
            except:
                pass
    
def main_process(accounts):
    for account in accounts:
        if account == "":
            continue
        driver = helper.start_browser()
        email = account.split(':')[0]
        password = account.split(':')[1]
        helper.outlook_login(driver, email, password)
        helper.check_popup(driver)
        helper.search_name(driver)
        click_link(driver)
        print("Finished:", email)
        driver.quit()
def main():
    accounts = open("accounts.txt", mode='r', encoding='utf-8').read().split('\n')
    random.shuffle(accounts)
    n = 50
    chunks = [accounts[i * n:(i + 1) * n] for i in range((len(accounts) + n - 1) // n )]
    thread_list = list()
    for chunk in chunks:
        t = threading.Thread(name='Thread', target=main_process, args=(chunk,))
        t.start()
        sleep(1)
        print ("t.name + ' started!'")
        thread_list.append(t)

    # Wait for all threads to complete
    for thread in thread_list:
        thread.join()

    print("Completed!")

if __name__ == '__main__':
    main()