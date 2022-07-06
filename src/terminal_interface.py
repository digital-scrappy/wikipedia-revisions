import sqlite3
import json
import pprint


db_path = "/home/scrappy/data/csh/bls/processed/oesm21nat.db"
con = sqlite3.connect(db_path)
cur = con.cursor()
table_name= "occupations"
input_column_name = "lenient_links"
flag_column_name = "selected_lenient_links"
output_column_name = "strict_links"


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


cur.execute(f"SELECT id, OCC_TITLE, lenient_links FROM {table_name} WHERE  {flag_column_name}= 0 AND length({input_column_name}) > 3")
data = cur.fetchall()
for occ in data:

    if not occ[2]:
        continue

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
                print(occ[0])

                value = json.dumps(good_links)
                cur.execute(f"UPDATE {table_name} SET {flag_column_name} = 1 WHERE id = ?", (occ[0],))
                cur.execute(f"UPDATE {table_name} SET  {output_column_name} = ? WHERE  id = ?", (value,
                                                                                                 occ[0]))
                con.commit()

                # cur.execute(
                #     f"INSERT INTO occupations Values (?, ?,?,?,1,0)", value)
                # cur.execute(
                #     f"UPDATE {table_name} SET cleaned_links = 1 WHERE  id = {occ[0]}")
                # con.commit()



con.close()
