import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn import linear_model, datasets
import statsmodels.api as sm
from statsmodels.formula.api import ols
from create_dataframes import dataframe_all, create_df_detailed

def completeness_detailed(df_all):
	df_detailed = create_df_detailed()
	df_all_detailed = df_all.loc[df_all['occ_group'] == "detailed"] 

	occ_dict = {}
	for occ_code in df_all_detailed["occ_code"].tolist():
		beginning = int(str(occ_code)[0:2])
		if beginning not in occ_dict:
			occ_dict[beginning] = [1]  
		elif beginning in occ_dict:
			occ_dict[beginning][0] += 1

	for occ_code in df_detailed["occ_code"].tolist():
		beginning = int(str(occ_code)[0:2])
		if len(occ_dict[beginning]) == 1:
			occ_dict[beginning].append(1)
		elif len(occ_dict[beginning]) == 2:
			occ_dict[beginning][1] += 1

	for key, item in occ_dict.items(): # adjust for missing matches
		if len(item) == 1:
			occ_dict[key].append(0)

	df_comp = pd.DataFrame(occ_dict).T
	df_comparisons = df_comp.rename(index={0: "all", 1: "matched"})

	_ = df_comparisons.plot(kind= 'bar' , secondary_y= 'matched', rot= 0 )
	plt.show()

def robust_regression(df, wiki_metric_var, race_gender_var):
    df = df.dropna()
    race_gender_var_lst = np.array(df[race_gender_var].tolist()).reshape(-1, 1)
    wiki_metric_var_lst = np.array(df[wiki_metric_var].tolist())
    
    # OLD PEARSON CODE
    # corr, p_value = pearsonr(race_gender_var_lst, wiki_metric_var_lst)
    # print('Pearsons correlation of the data: %.3f' % corr)
    # print("The p-value is", p_value)
    
    # REGRESSIONS
    # from here: https://medium.com/swlh/robust-regression-all-you-need-to-know-an-example-in-python-878081bafc0
    lr = linear_model.LinearRegression()
    lr.fit(race_gender_var_lst, wiki_metric_var_lst)
    
    # Robustly fit linear model with RANSAC algorithm
    ransac = linear_model.RANSACRegressor(random_state = 0)
    ransac.fit(race_gender_var_lst, wiki_metric_var_lst)
    inlier_mask = ransac.inlier_mask_
    outlier_mask = np.logical_not(inlier_mask)
    
    # Predict data of estimated models
    line_X = np.arange(race_gender_var_lst.min(), race_gender_var_lst.max(), 0.1)[:, np.newaxis]
    line_y = lr.predict(line_X)
    line_y_ransac = ransac.predict(line_X)
    # Compare estimated coefficients
    print("Estimated coefficients (linear regression, RANSAC):")
    print(lr.coef_, ransac.estimator_.coef_)
        
    lw = 2
    plt.scatter(race_gender_var_lst[inlier_mask], wiki_metric_var_lst[inlier_mask], color='yellowgreen', marker='.', label='Inliers')
    plt.scatter(race_gender_var_lst[outlier_mask], wiki_metric_var_lst[outlier_mask], color='gold', marker='.', label='Outliers')
    plt.plot(line_X, line_y, color='red', linewidth=lw, label='Regural Linear regression')
    plt.plot(line_X, line_y_ransac, color='royalblue', linewidth=lw, label='RANSAC regression')
    plt.legend(loc='upper right')
    plt.xlabel(str(race_gender_var))
    plt.ylabel(str(wiki_metric_var))
    plt.show()

    # OLD VIZ CODE
    # plt.scatter(race_gender_var_lst, wiki_metric_var_lst)
    # plt.xlabel(str(race_gender_var))
    # plt.ylabel(str(wiki_metric_var))
    # plt.show()
    
    
def multivariate_regression(df, col_list):
    corr_df = df[col_list]
    # create a string from the input col_list to make a multiple regression
    vars_string = ""
    for var in col_list[1:]:
        if var == col_list[-1]:
            vars_string += var
            break
        vars_string += (var + " + ")
    reg_string = str(col_list[0]) + " ~ " + vars_string
    results = ols(reg_string, data=corr_df).fit()
    print(results.summary())
    
    fig = sm.graphics.plot_partregress_grid(results)
    fig.tight_layout(pad=1.0) 
    
	
    
def simple_linear_regression(df, target, independent): 
    df_lr = df.dropna()
    
    corr, p_value = pearsonr(df_lr[target].tolist(), df_lr[independent].tolist())
    print('Pearsons correlation is %.3f' % corr)
    print("The p-value is", p_value)
    print()
    print()
    
    model = ols((str(target) + " ~ " + str(independent)), data = df_lr).fit()
    print(model.summary())

    sns.regplot(x = independent, y = target, data = df_lr)
    

# Taken from here:
# https://stackoverflow.com/questions/27694221/using-python-libraries-to-plot-two-horizontal-bar-charts-sharing-same-y-axis
def viz_sideways(df, target_variable, second_metric):
    df = df.dropna()
    
    occ_code = df["occ_code"].tolist()
    target_v = np.array(df[target_variable].tolist())
    second_m = df[second_metric].tolist()

    corr, p_value = pearsonr(target_v, second_m)
    print('Pearsons correlation is %.3f' % corr)
    print("The p-value is", p_value)    
    
    
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