import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

def viz_two_axes(df, target_variable, second_metric):
    df_viz = df.sort_values(by=[target_variable])
    df_viz.plot(kind="barh", x="occ_code", y=[target_variable, second_metric],
                secondary_y=[second_metric], rot=0)
    plt.show()


def viz_scatterplot_correlation(df, target_variable, second_metric):
    articles = df[second_metric].tolist()
    target = df[target_variable].tolist()

    corr, _ = pearsonr(target, articles)
    print('Pearsons correlation: %.3f' % corr)

    plt.scatter(articles, target)
    plt.show()


# Taken from here:
# https://stackoverflow.com/questions/27694221/using-python-libraries-to-plot-two-horizontal-bar-charts-sharing-same-y-axis

def viz_sideways(df, target_variable, second_metric):
    occ_code = df["occ_code"].tolist()
    target_v = np.array(df[target_variable].tolist())
    second_m = df[second_metric].tolist()

    idx = target_v.argsort()
    occ_code, target_v, second_m = [np.take(x, idx) for x in [occ_code, target_v, second_m]]
    y = np.arange(second_m.size)

    fig, axes = plt.subplots(ncols=2, sharey=True)
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