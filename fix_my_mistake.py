import pandas
import sqlite3
xls_path = "/home/scrappy/Downloads/oesm21nat/national_M2021_dl.xlsx"
new_db_path = "/home/scrappy/data/csh/bls/processed/new.db"
old_db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"
df = pandas.read_excel(xls_path)
df["computer_links"] = ""
df["human_links"] = ""
columns = ["index"] + [i.lower() for i in df.columns] + ["computer_links text","human_links text"]

con = sqlite3.connect(new_db_path)
cur = con.cursor()

# you get 1 cent for every sql injection attack you find in my code
cur.execute(f'CREATE TABLE IF NOT EXISTS occupations {tuple(columns)}')
df[df.O_GROUP == "detailed"].to_sql("occupations", con, if_exists = "replace", index = True)
con2 = sqlite3.connect(old_db_path)
old_cur = con2.cursor()
query = """SELECT * FROM cleaned_occupations_links_lenient WHERE length(selected_links) > 5"""
old_cur.execute(query)
data = old_cur.fetchall()

for occ in data:
    name = occ[1]
    human_links = occ[3]
    cur.execute("UPDATE occupations SET human_links = ? WHERE OCC_TITLE = ?", (human_links, name))
    con.commit()

    











