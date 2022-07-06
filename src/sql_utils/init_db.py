import sqlite3

def init_db(db_path):
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

    cur.execute('''CREATE TABLE cleaned_occupations_links_lenient(
                    id integer primary key,
                    name text,
                    candidate_links text,
                    selected_links text,
                    retrieved_candidate_links BIT,
                    cleaned_links BIT
    )''')

    cur.execute('''CREATE TABLE cleaned_occupations_links_strict(
                    id integer primary key,
                    name text,
                    candidate_links text,
                    selected_links text,
                    retrieved_candidate_links BIT,
                    cleaned_links BIT
    )''')
    con.close()
