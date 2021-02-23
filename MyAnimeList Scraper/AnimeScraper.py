from bs4 import BeautifulSoup
import requests
import sqlite3
import time


def scrape_single_page(page_limit):
    page_url = "https://myanimelist.net/topanime.php?limit="

    source = requests.get(page_url + str(page_limit)).text
    soup = BeautifulSoup(source, 'lxml')

    titles = soup.findAll(class_="hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3")
    results = []

    for clump in titles:
        results.append((clump.a.text, clump.a['href']))

    return results


def save_to_anime_db(results):
    conn = sqlite3.connect('anime.db')
    cursor = conn.cursor()

    for result in results:
        cursor.execute("""
                        INSERT INTO Anime
                        VALUES (? ,?)
                       """, result)

    conn.commit()
    conn.close()


def job(range_):
    for limit in range(0, range_, 50):
        time.sleep(5)
        save_to_anime_db(scrape_single_page(limit))
        if limit % 2000 == 0:
            time.sleep(180)
        print(limit / range_)


job(9000)
