from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import threading
import random
import helper


def new_contact_button(driver):
    while True:
        try:
            corner = driver.find_element_by_xpath("//*[@id='O365_MainLink_NavMenu']")
            break
        except:
            pass
    sleep(2)
    action = ActionChains(driver)
    action.move_to_element_with_offset(corner, 150, 75)
    action.click()
    action.perform()

def fill_form(driver, contact):
    new_contact_button(driver)
    name = contact.split('@')[0]
    print("Adding contact")
    while True:
        try:
            driver.find_element_by_id("GivenName").send_keys(name)
            driver.find_element_by_id("PersonaEmails1-0").send_keys(contact)
            driver.find_element_by_id("PersonaCompanyNames-0").send_keys("Malltsy")
            driver.find_element_by_xpath("/html/body/div[7]/div/div/div/div[2]/div[2]/main/section[2]/div[2]/div/button[1]/span/span/span").click()
            sleep(5)
            break
        except:
            pass

def add_contact(driver):
    contacts_url = "https://outlook.live.com/people"
    driver.get(contacts_url)
    contacts = open("to_contacts.txt", mode='r', encoding='utf-8').read().split('\n')
    for contact in contacts:
        fill_form(driver, contact)
        
def main_process(accounts):
    for account in accounts:
        if account == "":
            continue
        driver = helper.start_browser()
        email = account.split(':')[0]
        password = account.split(':')[1]
        helper.outlook_login(driver, email, password)
        print("Login successful")
        add_contact(driver)
        print("Contacts added successfully")
        driver.quit()

def main():
    accounts = open("accounts.txt", mode='r', encoding='utf-8').read().split('\n')
    random.shuffle(accounts)
    n = 25
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