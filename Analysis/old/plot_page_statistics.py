from datetime import datetime
from Occupation import Occupation
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt



def plot_page_stats(occ : Occupation):

    figure, axis = plt.subplots(4, 1)

    figure.suptitle(occ.occ_title ,fontweight ="bold")


    diffs = {**occ.strict_binned_diffs, **occ.lenient_binned_diffs}
    for page_name, stats in diffs.items():
        values  = list(stats.values())
        time_stamps = [month for month in stats.keys()]
        
        axis[0].plot(time_stamps, values, label=page_name, alpha=0.8)
    axis[0].set_title("diff")
    axis[0].legend(fontsize = "xx-small")

    edits = {**occ.strict_binned_edits, **occ.lenient_binned_edits}
    for page_name, stats in edits.items():
        values = list(stats.values())
        time_stamps = [month for month in stats.keys()]
        
        axis[1].plot(time_stamps, values, label=page_name, alpha=0.8)
    axis[1].set_title("edits")
    axis[1].legend(fontsize = "xx-small")



    oews_months =  [datetime(year = 2013+i, month = 5, day=1) for i in range(9)]
    oews_timestamps = [month for month in oews_months]
    a_mean = list(occ.A_MEDIAN) # changed to MEDIAN
    tot_emp = list(occ.TOT_EMP)
    oews_data_start = 9 - len(a_mean)
    
    axis[2].plot(oews_timestamps[oews_data_start:],a_mean,label="A_Mean")
    axis[2].set_title("A_Median")
    axis[2].legend(fontsize = "xx-small")

    axis[3].plot(oews_timestamps[oews_data_start:],tot_emp,label="TOT_EMP")
    axis[3].set_title("TOT_EMP")
    axis[3].legend(fontsize = "xx-small")

    figure.subplots_adjust(hspace=0.7)
    # figure.show()



