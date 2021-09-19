import os
import numpy as np
import pandas as pd
from numpy.random import normal
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns


HOME = os.getcwd()

df = pd.read_csv('export/factor_sensitivities.csv', index_col=0)

PORTFOLIO_LOSS = list()
Z = normal(loc=0.0, scale=1.0)
simulations = 5_000

for i in range(simulations):

    asset_value = list()
    for row in range(len(df)):
        epsilon = normal(loc=0.0, scale=1.0)
        asset_value.append(df['Factor_Sensitivity_MLE'].loc[row]*Z +
                           np.sqrt(1-pow(df['Factor_Sensitivity_MLE'].loc[row], 2))*epsilon)

    df['Asset_Value'] = asset_value

    default = list()
    for row in range(len(df)):
        if df['Asset_Value'].loc[row] < norm.ppf(df['PD'].loc[row]):
            default.append(1)
        else:
            default.append(0)

    df['Default'] = default

    loss = list()
    for row in range(len(df)):
        if df['Default'].loc[row] == 1:
            loss.append(df['LGD'].loc[row]*df['EAD'].loc[row])
        else:
            loss.append(0)

    df['Loss'] = loss

    df.to_csv(os.path.join(HOME, 'export', 'defaults.csv'))

    PORTFOLIO_LOSS.append(df['Loss'].sum())

plt.figure(figsize=(25, 10))
# plt.hist(PORTFOLIO_LOSS, bins=100)
sns.distplot(PORTFOLIO_LOSS, hist=True, kde=True, bins=100,
             color='darkblue',  hist_kws={'edgecolor': 'black'}, kde_kws={'linewidth': 4})
plt.xlabel('Portfolio Loss')
plt.ylabel('Density')
plt.title('Portfolio Loss Distribution')
plt.savefig(os.path.join(HOME, 'export', 'portfolio_loss_distribution.png'))
plt.show()
