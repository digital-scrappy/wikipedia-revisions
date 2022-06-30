import sqlite3
import json
import pprint


db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"
con = sqlite3.connect(db_path)
cur = con.cursor()
input_table_name = "occupations"
output_table_name = "cleaned_occupations_links_lenient"


def display_occupation(occ):

    keymap = {1: "e",
              2: "n",
              3: "a",
              4: "r",
              5: "i",
              6: "t",
              7: "u",
              8: "d",
              9: "c",
              0: "h"}
    name = occ[1]
    link_list = json.loads(occ[2])
    print("###################")
    print(name)
    print("###################")
    print("\n")

    for i in range(len(link_list)):
        print(f"{keymap[i]} - {link_list[i][0]} | {link_list[i][1]}")


def parse_answer(answer):
    reverse_keymap = {"e": 1,
                      "n": 2,
                      "a": 3,
                      "r": 4,
                      "i": 5,
                      "t": 6,
                      "u": 7,
                      "d": 8,
                      "c": 9,
                      "h": 0}
    answer_list = [reverse_keymap[char] for char in answer]

    return answer_list


def clean_links(input_table_name, output_table_name):
    query = f"SELECT * FROM {input_table_name} WHERE cleaned_links = 0"
    cur.execute(query)
    data = cur.fetchall()
    for occ in data:

        flag = "n"
        while flag != "y":

            display_occupation(occ)

            answer = input("link letters:")
            answer_list = [char for char in answer]
            false_answer_flag = False
            for char in answer_list:
                if char not in ['u', 'i', 'a', 'e', 'n', 'r', 't', 'd', 'c', 'h']:
                    print("wrong letter given")
                    false_answer_flag = True

            if not false_answer_flag:

                good_indices = parse_answer(answer)
                links = json.loads(occ[2])
                good_links = [links[i] for i in good_indices]
                pprint.pprint(good_links)

                flag = input("continue?(y/n):")
                if flag == "y":

                    value = (occ[0], occ[1], json.dumps(
                        links), json.dumps(good_links))
                    cur.execute(
                        f"INSERT INTO {output_table_name} Values (?, ?,?,?,1,0)", value)
                    cur.execute(
                        f"UPDATE {input_table_name} SET cleaned_links = 1 WHERE  id = {occ[0]}")
                    con.commit()


clean_links(input_table_name, output_table_name)

con.close()
