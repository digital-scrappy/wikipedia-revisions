import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np
import pandas as pd


def viz_scatterplot_correlation(df, target_variable, second_metric):
    df = df.dropna()
    target_v = df[target_variable].tolist()
    second_m = df[second_metric].tolist()

    corr, p_value = pearsonr(target_v, second_m)
    print('Pearsons correlation: %.3f' % corr)
    print("The p-value is", p_value)
    
    plt.scatter(second_m, target_v)
    plt.show()


# Taken from here:
# https://stackoverflow.com/questions/27694221/using-python-libraries-to-plot-two-horizontal-bar-charts-sharing-same-y-axis

def viz_sideways(df, target_variable, second_metric):
    df = df.dropna()
    
    occ_code = df["occ_code"].tolist()
    target_v = np.array(df[target_variable].tolist())
    second_m = df[second_metric].tolist()

    corr, _ = pearsonr(target_v, second_m)
    print('Pearsons correlation is %.3f' % corr)
    
    idx = target_v.argsort()
    occ_code, target_v, second_m = [np.take(x, idx) for x in [occ_code, target_v, second_m]]
    y = np.arange(second_m.size)

    fig, axes = plt.subplots(ncols = 2, sharey=True)
    axes[0].barh(y, target_v, align='center', color='blue', zorder=10)
    axes[0].set(title=str(target_variable))

    axes[1].barh(y, second_m, align='center', color='orange', zorder=10)
    axes[1].set(title=str(second_metric))

    axes[0].invert_xaxis()
    axes[0].set(yticks=y, yticklabels=occ_code)
    axes[0].yaxis.tick_right()

    for ax in axes.flat:
        ax.margins(0.03)
        ax.grid(True)
    fig.tight_layout()
    
    
def relative_positive_negative(df, target_variable, mapping_dict):
    relative_vals = [(value - mapping_dict[target_variable]) for value in df[target_variable]]
    
    plot_dict = {"code": df["occ_code"].tolist(), "values": relative_vals}    
    
    plot_df = pd.DataFrame.from_dict(plot_dict)
    plot_df.plot(x = "code", y = "values", kind = 'barh', figsize = (18, 10))
    
    
    
def viz_gender_target(df, target_var, second_metric, gender): # NAIVE ASSUMPTION (%women for each race)
    df_copy = df.dropna()
    if gender == "men" or gender == "women":
        df_copy[target_var] = df_copy[target_var].mul(df_copy[gender])

        print('Only for the gender "', gender.upper(), '"')
        viz_sideways(df_copy, target_var, second_metric)

    else:
        print("This function only works for women or men :/")