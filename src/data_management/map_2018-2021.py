import pandas
import sqlite3

xls_path = "/home/scrappy/Downloads/oesm21nat/national_M2021_dl.xlsx"
new_db_path = "/home/scrappy/data/csh/bls/processed/oesm21nat.db"
old_db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"
df = pandas.read_excel(xls_path)
df["computer_links"] = ""
df["lenient_links"] = ""
df["strict_links"] = ""
df["retrieved_candidate_links"] = 1
df["selected_computer_links"] = 1
df["selected_lenient_links"] = 0
extra_columns= ["computer_links text","lenient_links text","strict_links text" ,"retrieved_candidate_links BIT", "cleaned_links BIT"]
columns = ["id"] +[i.lower() for i in df.columns] + extra_columns

new_con = sqlite3.connect(new_db_path)
new_cur = new_con.cursor()

# you get 1 cent for every sql injection attack vector you find in my code
new_cur.execute(f'CREATE TABLE IF NOT EXISTS occupations {tuple(columns)}')

df[df.O_GROUP == "detailed"].to_sql("occupations", new_con, if_exists = "replace", index = True, index_label= "id")
old_con = sqlite3.connect(old_db_path)
old_cur = old_con.cursor()
query = """SELECT * FROM cleaned_occupations_links_lenient"""
old_cur.execute(query)
data = old_cur.fetchall()

for occ in data:
    _ , name, computer_links, human_links, _, _ = occ
    # name = occ[1]
    # human_links = occ[3]
    # computer_links = occ
    new_cur.execute("UPDATE occupations SET lenient_links = ? WHERE OCC_TITLE = ?", (human_links, name))
    new_cur.execute("UPDATE occupations SET computer_links = ? WHERE OCC_TITLE = ?", (computer_links, name))
    new_con.commit()

    











