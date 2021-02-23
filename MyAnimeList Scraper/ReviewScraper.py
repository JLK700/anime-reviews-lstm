from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

PATH = "C:/Users/Jan/PycharmProjects/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(PATH, chrome_options=chrome_options) 


def scrape_reviews_from_single_site(url):
    driver.get(url)
    revs = []
    try:
        buttons = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "js-toggle-review-button"))
        )

        for b in buttons:
            b.click()

    except:
        pass

    try:
        revs = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "borderDark"))
        )
    except:
        pass

    result = []
    for rev in revs:
        result.append(rev.text)

    return result


def get_anime_list():
    conn = sqlite3.connect('anime.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT rowid, Title, Url
                            FROM Anime
                            """)
    amine_list = cursor.fetchall()
    conn.commit()
    conn.close()
    return amine_list


def insert_to_review_db(insertion):
    conn = sqlite3.connect('anime.db')
    cursor = conn.cursor()

    cursor.execute("""
                    INSERT INTO Reviews
                    VALUES (? ,?, ?)
                   """, insertion)

    conn.commit()
    conn.close()


al = get_anime_list()
for index in range(4015, len(al)):
    anime = al[index]
    print(index)
    if index % 1000 == 999:
        time.sleep(120)
    if index % 5 == 0:
        time.sleep(1)

    curr_revs = scrape_reviews_from_single_site(anime[2])

    for review in curr_revs:
        insert_to_review_db((anime[0], review, "0"))
