import sqlite3
from datetime import datetime
from Occupation import Occupation
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
db_path = "/home/scrappy/data/csh/aggregated_edits.db"


oews_months =  [datetime(year = 2013+i, month = 5, day=1) for i in range(9)]
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute("Select * from occupations Where id = 18")
occ = Occupation(*cur.fetchone())

wiki_timestamps = [month.timestamp() for month in occ.strict_binned_diff.keys()]
oews_timestamps = [month.timestamp() for month in oews_months]

diffs = list(occ.strict_binned_diff.values())
edits = list(occ.strict_binned_edits.values())
a_mean = list(occ.A_MEAN)


# plt.plot(list(occ.lenient_binned_edits.keys())[:-1], occ.strict_binned_edits.values())
# plt.show()
# diffs = signal.detrend(diffs)
# edits = signal.detrend(edits)
# a_mean = signal.detrend(a_mean)

# diffs = diffs
# edits = edits
# a_mean = a_mean

figure, axis = plt.subplots(3, 1)

axis[0].plot(wiki_timestamps,diffs,label="diff")
axis[0].set_title("diff")
axis[0].legend()

axis[1].plot(wiki_timestamps,edits,label="diff")
axis[1].set_title("edits")
axis[1].legend()

axis[2].plot(oews_timestamps,a_mean,label="A_Mean")
axis[2].set_title("A_Mean")
axis[2].legend()
figure.suptitle(occ.occ_title ,fontweight ="bold")
for i in occ.strict_links:
    print(i[1])
figure.show()



