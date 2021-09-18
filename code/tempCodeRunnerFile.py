import os
import pandas as pd
from sqlalchemy import create_engine

_HOME = os.path.dirname(os.getcwd())
_URL = 'sqlite:///' + os.path.join(_HOME, 'data/PortfolioData.db')
engine = create_engine(_URL, echo=True)