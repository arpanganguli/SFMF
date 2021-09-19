"""The aim of this module is to calculate factor sensitvity, w_i. This is done using both the Maximum Likelihood Estimation (MLE) technique and calculating it from the Probabilty of Default.
    """

# ==============================================================================================================================================
# import relevant packages
from __init__ import ImportedDataframe, generate_standard_normal_rv
from sklearn.preprocessing import scale
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
from random import uniform
import matplotlib.pyplot as plt

# import relevant data

PortfolioData = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM PortfolioData')

Banks = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM Banks')

Consumer_Goods = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM ConsumerGoods')

REIT = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM REIT')

df = PortfolioData.copy()

# ==============================================================================================================================================
# Maximum Likelihood Method

# Standardised return of each sector
Banks_standardised_returns = scale(Banks['Change'])
Consumer_Goods_standardised_returns = scale(Consumer_Goods['Change'])
REIT_standardised_returns = scale(REIT['Change'])


# Calculating factor sensitivities for Banks
Banks_standardised_returns = scale(Banks['Change'])

n_iter = 1_000
w_Banks_list = list()

for i in range(n_iter):
    def mle_Banks(w_Banks):
        Z_Banks = generate_standard_normal_rv(Banks_standardised_returns)
        epsilon_Banks = generate_standard_normal_rv(Banks_standardised_returns)
        pred = (w_Banks*Z_Banks) + (np.sqrt(1-pow(w_Banks, 2))*epsilon_Banks)

        LL = np.sum(stats.norm.logpdf(Banks_standardised_returns, pred, 1))
        neg_LL = -1*LL
        return neg_LL
    random_seed = uniform(0.12, 0.24)
    mle_model = minimize(mle_Banks, np.array(random_seed), method='L-BFGS-B')
    x = mle_model.__getitem__('x')[0]

    w_Banks_list.append(x)


Banks_MLE_w_i = np.mean(w_Banks_list)

# Calculating factor sensitivities for Consumer Goods
Consumer_Goods_standardised_returns = scale(Consumer_Goods['Change'])

n_iter = 1_000
w_Consumer_Goods_list = list()

for i in range(n_iter):
    def mle_Consumer_Goods(w_Consumer_Goods):
        Z_Consumer_Goods = generate_standard_normal_rv(
            Consumer_Goods_standardised_returns)
        epsilon_Consumer_Goods = generate_standard_normal_rv(
            Consumer_Goods_standardised_returns)
        pred = (w_Consumer_Goods*Z_Consumer_Goods) + \
            (np.sqrt(1-pow(w_Consumer_Goods, 2))*epsilon_Consumer_Goods)

        LL = np.sum(stats.norm.logpdf(
            Consumer_Goods_standardised_returns, pred, 1))
        neg_LL = -1*LL
        return neg_LL
    random_seed = uniform(0.03, 0.16)
    mle_model = minimize(mle_Consumer_Goods, np.array(
        random_seed), method='L-BFGS-B')
    x = mle_model.__getitem__('x')[0]

    w_Consumer_Goods_list.append(x)


Consumer_Goods_MLE_w_i = np.mean(w_Consumer_Goods_list)


# Calculating factor sensitivities for Banks
REIT_standardised_returns = scale(REIT['Change'])

n_iter = 1_000
w_REIT_list = list()

for i in range(n_iter):
    def mle_REIT(w_REIT):
        Z_REIT = generate_standard_normal_rv(REIT_standardised_returns)
        epsilon_REIT = generate_standard_normal_rv(REIT_standardised_returns)
        pred = (w_REIT*Z_REIT) + (np.sqrt(1-pow(w_REIT, 2))*epsilon_REIT)

        LL = np.sum(stats.norm.logpdf(REIT_standardised_returns, pred, 1))
        neg_LL = -1*LL
        return neg_LL
    random_seed = uniform(0.12, 0.3)
    mle_model = minimize(mle_REIT, np.array(random_seed), method='L-BFGS-B')
    x = mle_model.__getitem__('x')[0]

    w_REIT_list.append(x)


REIT_MLE_w_i = np.mean(w_REIT_list)

# Adding factor sensitivities to dataframe
choices = [Banks_MLE_w_i, Consumer_Goods_MLE_w_i, REIT_MLE_w_i]
conditions = [df['Sector'] == 'Banks', df['Sector']
              == 'Consumer', df['Sector'] == 'Real Estate']

df['Factor_Sensitivity_MLE'] = np.select(conditions, choices)

# ==============================================================================================================================================

# Probabilty of Default Method assuming minimum correlation of 0.12 and maximum correlation of 0.24 - (0.12*((1 - np.exp(-50*df['PD'])) / (1 - np.exp(-50)))) + (0.24 * (1 - (1 - np.exp(-50*df['PD'])/(1 - np.exp(-50)))))

exponential = np.exp(-50 * pd.to_numeric(df['PD']))
common_fraction = (1 - exponential) / (1 - np.exp(-50))
df['Factor_Sensitivity_PD_Standard'] = (
    0.12 * common_fraction) + (0.24 * (1 - common_fraction))

# ==============================================================================================================================================

# Probabilty of Default Method assuming minimum correlation of [0.12, 0.24] for banks, [0.03, 0.16] for retail (consumer goods) and [0.12, 0.3] for real estate

exponential = np.exp(-50 * pd.to_numeric(df['PD']))
common_fraction = (1 - exponential) / (1 - np.exp(-50))
Banks_PD_custom_w_i = (0.12 * common_fraction) + (0.24 * (1 - common_fraction))
Consumer_Goods_PD_custom_w_i = (0.03 * common_fraction) + \
    (0.16 * (1 - common_fraction))
REIT_PD_custom_w_i = (0.12 * common_fraction) + (0.3 * (1 - common_fraction))

choices = [Banks_PD_custom_w_i,
           Consumer_Goods_PD_custom_w_i, REIT_PD_custom_w_i]
conditions = [df['Sector'] == 'Banks', df['Sector']
              == 'Consumer', df['Sector'] == 'Real Estate']
df['Factor_Sensitivity_PD_Custom'] = np.select(conditions, choices)

df.drop(df.index[100:999], inplace=True)
print(df)
