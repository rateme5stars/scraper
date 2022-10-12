from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json
import random


def random_sleep_time1():
    return round(random.random(), 2) * 5


def random_sleep_time2():
    return round(random.random(), 2) * 10


with open('celeb_name.txt', 'r') as celeb_file:
    names = celeb_file.readlines()

for i, name in enumerate(names):
    names[i] = name.replace('\n', '')

driver = webdriver.Chrome(ChromeDriverManager().install())
graph = list()

iter_num = 0
for name in names:
    print(name)
    cluster = {}
    neighbor_list = list()
    driver.get(f"https://www.google.com/search?q={name}")

    time.sleep(random_sleep_time2())
    job = driver.find_element(By.XPATH, value="//div[@class='wx62f PZPZlf x7XAkb']").text

    time.sleep(random_sleep_time1())
    see_more_bt = driver.find_element(By.XPATH, value='//g-more-link/../../a')
    see_more_bt.click()

    time.sleep(random_sleep_time1())
    see_more_list = driver.find_elements(By.XPATH, value='//g-scrolling-carousel/div/div/a')

    for idx, person in enumerate(see_more_list):
        neighbor = {}
        relevant_name = person.get_attribute('aria-label')

        time.sleep(random_sleep_time2())
        relevant_tab = driver.find_element(By.XPATH, value=f"//g-scrolling-carousel/div/div/a[contains(@aria-label, '{relevant_name}')]")
        relevant_tab.click()
        time.sleep(random_sleep_time1())
        title = driver.find_element(By.XPATH, value="//div[@class='wx62f PZPZlf x7XAkb']").text

        neighbor['job'] = title
        neighbor['rank'] = idx + 1
        neighbor['neighbor_name'] = relevant_name
        neighbor_list.append(neighbor)
    cluster['name'] = name
    cluster['job'] = job
    cluster['connections'] = neighbor_list
    graph.append(cluster)

with open('graph1.json', 'w', encoding='utf8') as fp:
    json.dump(graph, fp, ensure_ascii=False)

driver.quit()
