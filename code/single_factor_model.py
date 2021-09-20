"""This module generates the following - 
       1. Portfolio loss based on the Vasicek Single Factor Model;
       2. Plot of the portfolio loss distribution;
       3. Value-at-Risk for 95% and 99% confidence intervals.
    """
# ==============================================================================================================================================
# import relevant packages and files
import os
import numpy as np
import pandas as pd
from numpy.random import normal
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns


HOME = os.getcwd()

df = pd.read_csv('export/factor_sensitivities.csv', index_col=0)

# ==============================================================================================================================================
# Monte Carlo simulation
PORTFOLIO_LOSS = list()
Z = normal(loc=0.0, scale=1.0)
simulations = 10_000

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

# ==============================================================================================================================================

# Calculating Value-at-Risk (VaR) at 95% and 99% confidence intervals

VaR_95 = np.percentile(PORTFOLIO_LOSS, 95)
VaR_99 = np.percentile(PORTFOLIO_LOSS, 99)

# ==============================================================================================================================================

# Plotting the portfolio loss distribution

plt.figure(figsize=(25, 10))
# plt.hist(PORTFOLIO_LOSS, bins=100)
sns.histplot(PORTFOLIO_LOSS, kde=True, bins=100,
             color='darkblue')
plt.axvline(VaR_95)
plt.text(VaR_95, -0.4, 'VaR95', rotation=90)
plt.axvline(VaR_99)
plt.text(VaR_99, -0.4, 'VaR99', rotation=90)
plt.xlabel('Portfolio Loss')
plt.ylabel('Density')
plt.title('Portfolio Loss Distribution (10,000 simulations)')
plt.savefig(os.path.join(HOME, 'export',
            'portfolio_loss_distribution_10000.png'))
plt.show()
