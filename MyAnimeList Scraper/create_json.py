import sqlite3
import json
import regex as re


def create_json():
    conn = sqlite3.connect('anime.db')
    cursor = conn.cursor()

    cursor.execute("SELECT TEXT FROM REVIEWS")

    all_reviews = cursor.fetchall()
    all_reviews = all_reviews

    result = {}

    for index, review in enumerate(all_reviews):

        current_rev = review[0].split('\n')
        score = current_rev[2][-2:]
        score = (re.findall(r'\d+', score))
        if len(score) != 0:
            score = score[0]
            text = ''.join(current_rev[5:-3])
            result[index] = {'text': text, 'score': score}

    for k, v in result.items():
        print(k)
        print(v['text'])
        print(v['score'])

    print(len(result.items()))

    with open('anime_reviews.json', 'w') as json_file:
        json.dump(result, json_file)

    conn.commit()
    conn.close()


create_json()
