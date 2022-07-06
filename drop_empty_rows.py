import sqlite3

new_db_path = "/home/scrappy/data/csh/bls/processed/oesm21nat.db"
old_db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"

"oesm13nat"
"oesm14nat"
"oesm15nat"
"oesm16nat"
"oesm17nat"
"oesm18nat"
"oesm19nat"
"oesm20nat"
"oesm21nat"
old_con = sqlite3.connect(old_db_path)
old_cur = old_con.cursor()
new_con = sqlite3.connect(new_db_path)
new_cur = new_con.cursor()

occ_columns = [ "OCC_CODE", "OCC_TITLE", "TOT_EMP", "H_MEAN", "A_MEAN","H_PCT10", "H_PCT25", "H_MEDIAN", "H_PCT75","H_PCT90", "A_PCT10", "A_PCT25", "A_MEDIAN", "A_PCT75","A_PCT90"]
my_columns = ["lenient_links", "strict_links"]
cur.execute(f"SELECT {my_columns} FROM {table_name} WHERE  {flag_column_name}= 0 AND length({input_column_name}) > 3")
data = cur.fetchall()
for occ in data:
