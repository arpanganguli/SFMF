import os
import pandas as pd
from sqlalchemy import create_engine

_HOME = os.path.dirname(os.getcwd())
_URL = 'sqlite:///' + os.path.join(_HOME, 'SFMF/data/PortfolioData.db')
engine = create_engine(_URL, echo=True)

query_string = "SELECT * FROM RWA_Input_Data "
df = pd.read_sql(sql=query_string, con=engine)
print(df.head())
