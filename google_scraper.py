from random import uniform
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

with open('celeb_name.txt', 'r') as celeb_file:
    names = celeb_file.readlines()

for i, name in enumerate(names):
    names[i] = name.replace('\n', '')

driver = webdriver.Chrome(ChromeDriverManager().install())
graph = list()

start_process = time.time()
for name in names:
    start_celeb = time.time()
    cluster = {}
    neighbor_list = list()
    driver.get(f"https://www.google.com/search?q={name}")

    time.sleep(uniform(5, 6))

    try:
        print(f'--- Getting {name} Information ---')
        job = driver.find_element(By.XPATH, value='//div[@class="wx62f PZPZlf x7XAkb"]').text
        see_more_bt = driver.find_element(By.XPATH, value="//g-more-link/../../a")
        see_more_bt.click()
        time.sleep(uniform(2, 3))
        see_more_list = driver.find_elements(By.XPATH, value="//g-scrolling-carousel/div/div/a")
    except Exception as error:
        job = 'Unknown'
        print(f'There is an error with {name}')
        continue

    print('--- Getting The Relevants Information ---')
    for idx, person in enumerate(see_more_list):
        neighbor = {}
        try:
            relevant_name = person.get_attribute('aria-label')
            relevant_tab = driver.find_element(By.XPATH, value=f'//g-scrolling-carousel/div/div/a[contains(@aria-label, "{relevant_name}")]')
            relevant_tab.click()
            time.sleep(uniform(2, 3))
            title = driver.find_element(By.XPATH, value='//div[@class="wx62f PZPZlf x7XAkb"]').text
        except Exception as error:
            title = 'Unknown'
            print(f'There is an error with {relevant_name}')
            continue

        neighbor['job'] = title
        neighbor['rank'] = idx + 1
        neighbor['neighbor_name'] = relevant_name
        neighbor_list.append(neighbor)

    cluster['name'] = name
    cluster['job'] = job
    cluster['connections'] = neighbor_list
    graph.append(cluster)

    end_celeb = time.time()
    print(f'Done: {end_celeb-start_celeb}\n')

with open('graph2.json', 'w', encoding='utf8') as fp:
    json.dump(graph, fp, ensure_ascii=False)
end_process = time.time()

print(f'Crawling duration: {end_process - start_process}')
driver.quit()
