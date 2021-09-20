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
simulations = 1000

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

    PORTFOLIO_LOSS.append(df['Loss'].sum())

# ==============================================================================================================================================

# Calculating Value-at-Risk (VaR) and Expected Shortfall (ES) at 95% and 99% confidence intervals

VaR_90 = np.percentile(PORTFOLIO_LOSS, 90)
VaR_i = 0
steps_i = np.linspace(90, 100, 10_000)
for i in steps_i:
    VaR_i += (np.percentile(PORTFOLIO_LOSS, i))
ES_90 = VaR_i/10_000

VaR_999 = np.percentile(PORTFOLIO_LOSS, 99.9)
VaR_j = 0
steps_j = np.linspace(99.9, 100, 10_000)
for j in steps_j:
    VaR_j += (np.percentile(PORTFOLIO_LOSS, j))
ES_999 = VaR_j/10_000
# ==============================================================================================================================================

print(PORTFOLIO_LOSS)

# Plotting the portfolio loss distribution

plt.figure(figsize=(25, 10))
# plt.hist(PORTFOLIO_LOSS, bins=100)
sns.histplot(PORTFOLIO_LOSS, kde=True, bins=100,
             color='darkblue')
plt.axvline(VaR_90)
plt.text(VaR_90, -0.4, 'VaR 90%', rotation=90)
plt.axvline(VaR_999)
plt.text(VaR_999, -0.4, 'VaR 99.9%', rotation=90)
plt.axvline(ES_90)
plt.text(ES_90, -0.4, 'ES 90%', rotation=90)
plt.axvline(ES_999)
plt.text(ES_999, -0.4, 'ES 99.9%', rotation=90)
plt.xlabel('Portfolio Loss')
plt.ylabel('Frequency')
plt.title('Portfolio Loss Distribution (1,000 simulations)')
plt.savefig(os.path.join(HOME, 'export',
            'portfolio_loss_distribution_1000.png'))
plt.show()
