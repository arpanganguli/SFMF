"""The aim of this module is to calculate factor sensitvity, w_i. This is done using both the Maximum Likelihood Estimation (MLE) technique and calculating it from the Probabilty of Default.
    """

# import relevant packages
from __init__ import ImportedDataframe
from sklearn.preprocessing import scale
import numpy as np
import pandas as pd

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

# Maximum Likelihood Method

# Standardised return of each sector
Banks_standardised_returns = scale(Banks['Change'])
Consumer_Goods_standardised_returns = scale(Consumer_Goods['Change'])
REIT_standardised_returns = scale(REIT['Change'])


# Calculating factor sensitivities for each sector

Banks_MLE_w_i = Banks_standardised_returns.mean()
Consumer_Goods_MLE_w_i = Consumer_Goods_standardised_returns.mean()
REIT_MLE_w_i = REIT_standardised_returns.mean()

# Adding factor sensitivities to dataframe

choices = [Banks_MLE_w_i, Consumer_Goods_MLE_w_i, REIT_MLE_w_i]
conditions = [df['Sector'] == 'Banks', df['Sector']
              == 'Consumer', df['Sector'] == 'Real Estate']

df['Factor_Sensitivity_MLE'] = np.select(conditions, choices)

# Probabilty of Default Method assuming minimum correlation of 0.12 and maximum correlation of 0.24 - (0.12*((1 - np.exp(-50*df['PD'])) / (1 - np.exp(-50)))) + (0.24 * (1 - (1 - np.exp(-50*df['PD'])/(1 - np.exp(-50)))))

exponential = np.exp(-50 * pd.to_numeric(df['PD']))
common_fraction = (1 - exponential) / (1 - np.exp(-50))
df['Factor_Sensitivity_PD_Standard'] = (
    0.12 * common_fraction) + (0.24 * (1 - common_fraction))

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
