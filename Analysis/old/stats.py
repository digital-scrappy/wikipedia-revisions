import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from create_df_for_non_ipynb import create_dataframe

sns.set_theme(style="white")

df = create_dataframe()
corr_df = df[["art_per_detailed", "avg_unique_auths", "avg_page_lengths", "women", "african_american", "asian", "hispanic", "non_hispanic_white"]].apply(pd.to_numeric)
corr_df.dropna(inplace = True)
print(corr_df.head(5))
corr = corr_df.corr(min_periods = 0)


# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

f.show()
f.waitforbuttonpress()