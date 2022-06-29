import sqlite3

db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"

con = sqlite3.connect(db_path)
cur = con.cursor()

query = "SELECT * FROM occupations WHERE retrieved_candidate_links = 0"


cur.execute(query)

print(cur.fetchall())
con.close()
