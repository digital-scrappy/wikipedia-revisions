import sqlite3
import json
from scipy.stats import spearmanr
from numpy import mean, diff
import pandas as pd


new_db_path = "/home/scrappy/data/csh/aggregated_edits.db"

con = sqlite3.connect(new_db_path)
cur = con.cursor()


query = f"SELECT occ_title, strict_edit_sum, tot_emp, a_mean FROM occupations "

cur.execute(query)
data = cur.fetchall()
df = pd.DataFrame({"occ_title": [],
                   "stric_edit_sum": [],
                   "tot_emp": [],
                   "a_mean": [],
                   "rho_emp" : [],
                   "rho_wage" : [],
                   "rho_emp_diff" : [],
                   "rho_wage_diff" : [],
                   "pval_emp" : [],
                   "pval_wage" : [],
                   "pval_emp_diff" : [],
                   "pval_wage_diff" : []})
                   

for occ in data:
    occ_title = occ[0]
    edit_sum = json.loads(occ[1])
    tot_emp = json.loads(occ[2])
    a_mean = json.loads(occ[3])

    if len(tot_emp) != len(edit_sum) or len(a_mean) != len(edit_sum):
        continue
    all_lists = edit_sum.copy() + tot_emp.copy() + a_mean.copy()
    if not all([isinstance(item, int) for item in all_lists ]):
        continue
    '''
o
                   "stric_edit_sum": [],
                   "tot_emp": [],
                   "a_mean": [],
                   "rho_epm" : [],
                   "rho_wage" : [],
                   "rho_emp-diff" : [],
                   "rho_wage-diff" : []
                   "pval_epm" : [],
                   "pval_wage" : [],
                   "pval_emp_diff" : [],
                   "pval_wage_diff" : []})

'''
    rho, pval = spearmanr(edit_sum, tot_emp)
    rho_emp = rho
    pval_emp = pval

    rho, pval = spearmanr(edit_sum[1:], diff(tot_emp))
    rho_emp_diff = rho
    pval_emp_diff = pval

    rho, pval = spearmanr(edit_sum, a_mean)
    rho_wage = rho
    pval_wage = pval

    rho, pval = spearmanr(edit_sum[1:], diff(a_mean))
    rho_wage_diff = rho
    pval_wage_diff = pval

    df.loc[len(df.index)] = [occ_title, edit_sum,
                             tot_emp, a_mean,
                             rho_emp, rho_wage,
                             rho_emp_diff, rho_wage_diff,
                             pval_emp, pval_wage,
                             pval_emp_diff, pval_wage_diff] 


