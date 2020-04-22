from selenium import webdriver
import time
import string
import random
import re
import json
import threading
from datetime import datetime


# BOT
CHKNET = "https://web2.chknet.eu/"
enabled = True
channel_name = "#unix"
bot_name = "%s%i" % (''.join(random.choices(
    string.ascii_uppercase + string.digits, k=10)), random.randint(0, 9999))


# DRIVER
driver_options = webdriver.ChromeOptions()
driver_options.headless = True
driver_options.add_argument('--silent')
driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(chrome_options=driver_options)


try:
    print("[!] Connecting to chknet...")
    driver.get(CHKNET)
    time.sleep(3)
    driver.find_element_by_id('viewport')

except:
    print("[!] Error trying to connect to webchknet")

time.sleep(10)


# LOGIN
driver.find_element_by_name('nick').clear()
driver.find_element_by_name('nick').send_keys(bot_name)

driver.find_element_by_name('username').clear()
driver.find_element_by_name('username').send_keys(bot_name)

driver.find_element_by_name('join').clear()
driver.find_element_by_name('join').send_keys(channel_name)

driver.find_element_by_css_selector('.btn').click()

time.sleep(5)  # wait chknet app load


# GO TO #UNIX CHANNEL
channels = driver.find_elements_by_css_selector('.channel-list-item')
print("[!] Connected with chknet!")
for channel in channels:
    if channel.get_attribute('data-name') == channel_name:
        channel.click()
        print("[!] Joined #unix")
        break


# GRAB CC'S
approved_cc_regex = r"[0-9]{15,16}\s[0-9]{4}\s[0-9]{3,4}\s\-\s.*\s\-\sApproved"
ccs = []


def save():
    filepath = "ccs_%s.txt" % datetime.now().strftime('%Y_%m_%d-%H_%M_%S')

    with open(filepath, 'a') as output:
        for cc in ccs:
            output.write("%s\n" % cc)

    print("[!] Credit cards were dumped to %s" % (filepath))

    time.sleep(4)


def grab():

    while driver.page_source:
        try:
            approveds = re.finditer(
                approved_cc_regex, driver.page_source, re.MULTILINE)
            approveds = [approved.group() for approved in approveds]

            for approved in approveds:
                if approved not in list(ccs):
                    print("[chknet-capture] %s" % approved)
                    ccs.append(approved)

            time.sleep(3)
        except KeyboardInterrupt:
            if len(ccs) > 0:
                save()
            enabled = False
            driver.quit()
            exit()

        except Exception as e:
            if len(ccs) > 0:
                save()
            enabled = False
            driver.quit()

    print("[!] An error occurred during the process: %s" % str(e.__str__))
    exit()


t = threading.Thread(target=grab)
t.start()
