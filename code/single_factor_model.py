import os
import pandas as pd
from sqlalchemy import create_engine

# import data

_HOME = os.path.dirname(os.getcwd())
_URL = 'sqlite:///' + os.path.join(_HOME, 'SFMF/data/database.db')
engine = create_engine(_URL, echo=True)

query_string_PortfolioData = "SELECT * FROM PortfolioData"
query_string_CovarianceMatrix = "SELECT * FROM CovarianceMatrix"
query_string_RSqSens = "SELECT * FROM RSqSens"
PortfolioData = pd.read_sql(sql=query_string_PortfolioData, con=engine)
CovarianceMatrix = pd.read_sql(sql=query_string_CovarianceMatrix, con=engine)
RSqSens = pd.read_sql(sql=query_string_RSqSens, con=engine)
