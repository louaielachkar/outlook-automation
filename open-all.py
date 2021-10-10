from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import threading
import random
import helper

def mark_read(driver):
    while True:
        try:
            try:
                driver.find_element_by_xpath("//span[text()='Mark all as read']").click()
            except NoSuchElementException:
                driver.find_element_by_xpath("//span[text()='Marquer tout comme lu']").click()
            sleep(3)
            try:
                driver.find_element_by_xpath("/html/body/div[7]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/span[1]/button/span").click()
                sleep(3)
            except NoSuchElementException:
                pass
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
        mark_read(driver)
        try:
            driver.find_element_by_xpath("//*[@id='Pivot26-Tab1']/span/div/div/span/span").click()
            mark_read(driver)
        except NoSuchElementException:
            pass
        sleep(5)
        print("Finished:", email)
        driver.quit()

def main():
    accounts = open("accounts.txt", mode='r', encoding='utf-8').read().split('\n')
    random.shuffle(accounts)
    n = 15
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

