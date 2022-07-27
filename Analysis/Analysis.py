#!/usr/bin/env python
# coding: utf-8


import sqlite3
from datetime import datetime
from Occupation import Occupation
import json 

from matplotlib import pyplot as plt
from get_page_length_subset_indices import get_subset_indices
from plot_page_statistics import plot_page_stats
from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets







def plot_page(occ_list, idx):
    occ = Occupation(*occ_list[idx])
    print(occ.lenient_links)
    print(occ.strict_links)
    plot_page_stats(occ)
    
    




db_path = "/home/scrappy/data/csh/aggregated_edits.db"


page_indices = [ i  for i in  get_subset_indices("test.json",10000)]


con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute(f"Select * from occupations Where id IN {tuple(page_indices)}")
occupations = cur.fetchall()





plot_page(occupations, 20)






