from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

names = ['T-ara']
driver = webdriver.Chrome(ChromeDriverManager().install())

graph = list()

for name in names:
    cluster = {}
    neighbor_list = list()
    driver.get(f"https://www.google.com/search?q={name}")
    time.sleep(3)

    job = driver.find_element(By.XPATH, value="//div[@class='wx62f PZPZlf x7XAkb']").text
    see_more_bt = driver.find_element(By.XPATH, value='//g-more-link/../../a')
    see_more_bt.click()

    see_more_list = driver.find_elements(By.XPATH, value='//g-scrolling-carousel/div/div/a')

    for idx, person in enumerate(see_more_list):
        neighbor = {}
        relevant_name = person.get_attribute('aria-label')

        time.sleep(2)
        relevant_tab = driver.find_element(By.XPATH, value=f"//g-scrolling-carousel/div/div/a[contains(@aria-label, '{relevant_name}')]")
        relevant_tab.click()
        time.sleep(2)
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
print(cluster)
