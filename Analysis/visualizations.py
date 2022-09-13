import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn import linear_model, datasets


def viz_scatterplot_correlation(df, race_gender_var, wiki_metric_var):
    df = df.dropna()
    race_gender_var_lst = np.array(df[race_gender_var].tolist()).reshape(-1, 1)
    wiki_metric_var_lst = np.array(df[wiki_metric_var].tolist())

    # OLD PEARSON CODE
    # corr, p_value = pearsonr(race_gender_var_lst, wiki_metric_var_lst)
    # print('Pearsons correlation of the data: %.3f' % corr)
    # print("The p-value is", p_value)
    
    # REGRESSIONS
    # Fit line using all data
    lr = linear_model.LinearRegression()
    lr.fit(race_gender_var_lst, wiki_metric_var_lst)
    
    # Robustly fit linear model with RANSAC algorithm
    ransac = linear_model.RANSACRegressor()
    ransac.fit(race_gender_var_lst, wiki_metric_var_lst)
    inlier_mask = ransac.inlier_mask_
    outlier_mask = np.logical_not(inlier_mask)
    
    # Predict data of estimated models
    line_X = np.arange(race_gender_var_lst.min(), race_gender_var_lst.max())[:, np.newaxis]
    line_y = lr.predict(line_X)
    line_y_ransac = ransac.predict(line_X)
    # Compare estimated coefficients
    print("Estimated coefficients (linear regression, RANSAC):")
    print(lr.coef_, ransac.estimator_.coef_)
    
    
    lw = 2
    plt.plot(line_X, line_y, color='navy', linewidth=lw, label='Regural Linear regression')
    plt.plot(line_X, line_y_ransac, color='royalblue', linewidth=lw, label='RANSAC regression')
    
    plt.scatter(race_gender_var_lst[inlier_mask], wiki_metric_var_lst[inlier_mask], color='yellowgreen', marker='.', label='Inliers')
    plt.scatter(race_gender_var_lst[outlier_mask], wiki_metric_var_lst[outlier_mask], color='gold', marker='.', label='Outliers')

    plt.legend(loc='upper right')
    plt.xlabel(str(race_gender_var))
    plt.ylabel(str(wiki_metric_var))
    plt.show()

    # OLD VIZ CODE
    # plt.scatter(race_gender_var_lst, wiki_metric_var_lst)
    # plt.xlabel(str(race_gender_var))
    # plt.ylabel(str(wiki_metric_var))
    # plt.show()


    
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