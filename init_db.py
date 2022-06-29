import sqlite3
db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"

con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute('''CREATE TABLE occupations(
                id integer primary key,
                name text,
                candidate_links text,
                selected_links text,
                retrieved_candidate_links BIT,
                cleaned_links BIT
)''')
con.close()
